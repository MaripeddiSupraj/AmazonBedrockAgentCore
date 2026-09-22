import os
import json
import logging
import base64
import requests
import boto3
from flask import Flask, request, jsonify
from bedrock_agentcore import BedrockAgentCoreApp

# --------------------------------------------------
# AgentCore runtime requirement (container requirement)
# --------------------------------------------------
agent = BedrockAgentCoreApp()

# --------------------------------------------------
# Setup Flask + logging
# --------------------------------------------------
flask_app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
werkzeug_log = logging.getLogger("werkzeug")

# --------------------------------------------------
# AWS + Config
# --------------------------------------------------
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
GATEWAY_URL = os.environ.get("GATEWAY_URL")
AGENT_SECRET = os.environ.get("AGENT_SECRET")
MODEL_ID = "global.anthropic.claude-sonnet-4-5-20250929-v1:0" 

PAYMENT_MANAGER_ARN = os.environ.get("PAYMENT_MANAGER_ARN")
PAYMENT_INSTRUMENT_ID = os.environ.get("PAYMENT_INSTRUMENT_ID")

bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)
secrets = boto3.client("secretsmanager", region_name=AWS_REGION)
agentcore = boto3.client("bedrock-agentcore", region_name=AWS_REGION)
PAYMENT_SESSIONS_CACHE = {}

# --------------------------------------------------
# JSON Extraction Helper
# --------------------------------------------------
def extract_json(text: str):
    if not text:
        return None
    text = text.strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    s = text.find('[')
    e = text.rfind(']')
    if s != -1 and e != -1 and e > s:
        try:
            return json.loads(text[s:e+1])
        except Exception:
            pass

    s = text.find('{')
    e = text.rfind('}')
    if s != -1 and e != -1 and e > s:
        try:
            return json.loads(text[s:e+1])
        except Exception:
            pass

    return None

# --------------------------------------------------
# OAuth Token
# --------------------------------------------------
def get_oauth_token():
    secret_value = secrets.get_secret_value(SecretId=AGENT_SECRET)
    secret = json.loads(secret_value["SecretString"])

    auth = base64.b64encode(
        f"{secret['CLIENT_ID']}:{secret['CLIENT_SECRET']}".encode()
    ).decode()

    headers = {
        "Authorization": "Basic " + auth,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": secret["SCOPE"]
    }

    response = requests.post(secret["TOKEN_URL"], headers=headers, data=data, timeout=30)
    response.raise_for_status()
    return response.json()["access_token"]

# --------------------------------------------------
# Gateway Tool Functions (FIXED FOR DUPLICATE COOKIE ERROR)
# --------------------------------------------------
def list_tools(token: str, payment_session_id: str = None):
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type": "application/json"
    }
    
    if payment_session_id:
        headers["X-Payment-Session-Id"] = payment_session_id
        
    response = requests.post(GATEWAY_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json().get("result", {}).get("tools", [])

def call_tool(token: str, name: str, arguments: dict, payment_session_id: str = None):
    logger.info(f"TOOL CALL → {name} | args={json.dumps(arguments)}")

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments}
    }

    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type": "application/json"
    }
    
    if payment_session_id:
        headers["X-Payment-Session-Id"] = payment_session_id

    # --- SAFETY FILTER INJECTED HERE ---
    try:
        response = requests.post(GATEWAY_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
        
    except json.JSONDecodeError:
        error_text = response.text or ""
        # Catch the AgentCore duplicate cookie error text signature
        if "duplicate key" in error_text or "Set-Cookie" in error_text:
            logger.error("Intercepted internal AgentCore duplicate Set-Cookie validation crash.")
            return {
                "jsonrpc": "2.0",
                "id": 1,
                "error": {
                    "code": -32000,
                    "message": "CDPBazaar backend response parsing failed due to duplicate Set-Cookie headers."
                }
            }
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "error": {
                "code": -32603,
                "message": f"Gateway structural crash: {error_text[:150]}"
            }
        }
    except Exception as e:
        logger.error(f"HTTP request failed for tool {name}: {str(e)}")
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "error": {
                "code": -32603,
                "message": f"Internal tool execution error: {str(e)}"
            }
        }

def call_llm(messages):
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": messages,
        "max_tokens": 800,
        "temperature": 0.2
    }

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body).encode("utf-8"),
        contentType="application/json",
        accept="application/json"
    )

    data = json.loads(response["body"].read())
    content = data.get("content", "")
    if isinstance(content, list) and content:
        return content[0].get("text", "")
    return content

# --------------------------------------------------
# Slack Tool Detection
# --------------------------------------------------
def is_slack_post_tool(tool_name: str, tool_def: dict) -> bool:
    name = (tool_name or "").lower()
    desc = (tool_def.get("description") or "").lower()
    return (
        ("slack" in name and ("post" in name or "message" in name))
        or ("slack" in desc and "message" in desc)
    )

# --------------------------------------------------
# Main Agent Execution
# --------------------------------------------------
def run_agent(user_text, token, payment_session_id=None):
    tools = list_tools(token, payment_session_id)
    tool_defs_by_name = {t.get("name"): t for t in tools if t.get("name")}

    decision_prompt = f"""
You are an AI agent with multiple tools.

TOOLS AVAILABLE:
{json.dumps(tools, indent=2)}

STRICT OPERATIONAL GUARDRAILS:
1. ONLY call tools that contain the prefix or namespace 'CDPBazaar' if the user input explicitly mentions the keywords "Bazaar", "CDPBazaar", or "Premium Data".
2. For all generic requests involving geographic coordinates, locations, simple data, quotes, or weather forecasting (e.g., Madrid, Mumbai, Tokyo, surfing, motivational quotes), rely EXCLUSIVELY on your 'LocationCoordinates' and 'Slack' tools. 
3. DO NOT attempt to call 'CDPBazaar___search_resources' or look for premium datasets for generic user questions unless explicit marketplace access is requested.

RULES:
- Return ONLY a JSON list.
- Each item must be either:

1. Tool call:
   {{
     "action": "tool",
     "name": "<exact tool name>",
     "arguments": {{...}}
   }}

2. Final answer:
   {{
     "action": "answer"
   }}

If the user explicitly provides Slack message content,
call the Slack tool directly using that content.

No extra text.

USER INPUT:
{user_text}
"""

    raw = call_llm([{"role": "user", "content": decision_prompt}])
    actions = extract_json(raw)

    if not actions:
        return call_llm([{"role": "user", "content": user_text}])

    if not isinstance(actions, list):
        actions = [actions]

    tool_outputs = []
    slack_calls = []
    tools_used = False

    for action in actions:
        if action.get("action") == "tool":
            tools_used = True
            name = action.get("name")
            args = action.get("arguments", {}) or {}
            tool_def = tool_defs_by_name.get(name, {})

            if is_slack_post_tool(name, tool_def):
                slack_calls.append((name, args))
                continue

            result = call_tool(token, name, args, payment_session_id)
            tool_outputs.append({"name": name, "result": result})

        elif action.get("action") == "answer" and not tools_used:
            return call_llm([{"role": "user", "content": user_text}])

    # --------------------------------------------------
    # Step 2: Slack Handling (RECOVERED FOR FORCED ALERTS)
    # --------------------------------------------------
    if slack_calls:
        if not tool_outputs:
            for name, args in slack_calls:
                if not args.get("text"):
                    args["text"] = user_text
                result = call_tool(token, name, args, payment_session_id)
                tool_outputs.append({"name": name, "result": result})
        else:
            # Check if our new custom error signature triggered in Part 1
            has_errors = any(
                isinstance(out.get("result"), dict) and "error" in out["result"] 
                for out in tool_outputs
            )

            if has_errors:
                logger.warning("Upstream gateway error detected. Creating alert update for Slack.")
                final_slack_message = (
                    "⚠️ *Data Sync Alert*:\n"
                    "The agent attempted to fetch premium data from CDPBazaar, but the request was blocked "
                    "by a strict header collision (`duplicate key: Set-Cookie`) in the AgentCore Gateway integration.\n"
                    "The main task execution loop has been recovered safely."
                )
            else:
                slack_prompt = f"""
Generate the final message to be delivered externally.

STRICT RULES:
- Use ONLY factual data from tool results.
- Do NOT invent anything.
- Do NOT include placeholders.
- Do NOT include raw JSON.
- Return plain text only.

User request:
{user_text}

Tool results:
{json.dumps(tool_outputs, indent=2)}
"""
                final_slack_message = call_llm([{"role": "user", "content": slack_prompt}]).strip()

            # Dispatches the alert to Slack so the step is never skipped
            for name, args in slack_calls:
                args["text"] = final_slack_message
                try:
                    result = call_tool(token, name, args, payment_session_id)
                    tool_outputs.append({"name": name, "result": result})
                except Exception as slack_err:
                    logger.error(f"Failed to post update to Slack tool {name}: {slack_err}")

    # --------------------------------------------------
    # Step 3: Final Response
    # --------------------------------------------------
    summary_prompt = f"""
Answer the user's original request clearly.

- Do NOT mention tool names.
- Do NOT include raw JSON.
- If Slack posting occurred successfully, state that it has been sent.
- If Slack failed, clearly state the reason.
- Use past tense.

User question:
{user_text}

Tool results:
{json.dumps(tool_outputs, indent=2)}
"""

    final_answer = call_llm([{"role": "user", "content": summary_prompt}])
    return final_answer

# --------------------------------------------------
# Flask Endpoints
# --------------------------------------------------
@flask_app.route("/", methods=["POST"])
def root():
    return invocations()

@flask_app.route("/invocations", methods=["POST"])
def invocations():
    payload = request.get_json() or {}
    user_text = payload.get("input", {}).get("text", "")
    chat_session_id = payload.get("sessionId", "default-lab-thread")

    payment_session_id = None
    
    if chat_session_id in PAYMENT_SESSIONS_CACHE:
        payment_session_id = PAYMENT_SESSIONS_CACHE[chat_session_id]
        logger.info(f"Reusing existing Payment Session: {payment_session_id} for Chat Thread: {chat_session_id}")
    else:
        try:
            session_res = agentcore.create_payment_session(
                paymentManagerArn=PAYMENT_MANAGER_ARN,
                userId="lab-session-agent-01",
                expiryTimeInMinutes=60,       
                limits={                      
                    "maxSpendAmount": {
                        "value": "0.05",
                        "currency": "USD"
                    }
                }
            )
            payment_session_id = session_res["paymentSession"]["paymentSessionId"]
            PAYMENT_SESSIONS_CACHE[chat_session_id] = payment_session_id
            logger.info(f"New Payment Session Generated: {payment_session_id} for Chat Thread: {chat_session_id}")
        except Exception as e:
            logger.error(f"Failed to generate payment session: {e}")
            payment_session_id = None

    token = get_oauth_token()
    result = run_agent(user_text, token, payment_session_id)

    return jsonify({"completion": result, "stop_reason": "end_turn"}), 200

@flask_app.route("/ping", methods=["GET"])
def ping():
    werkzeug_log.disabled = True
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=8080)
