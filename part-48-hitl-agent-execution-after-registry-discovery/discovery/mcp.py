import itertools
import json
import boto3
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

# ---------------------------------------------------------------------------
# Global Constants
# ---------------------------------------------------------------------------
REGION = "us-east-1"
SERVICE = "agent-registry"
MCP_PROTOCOL_VERSION = "2025-11-25"
_ids = itertools.count(1)


def mcp_call(endpoint, region, creds, registry_id, method, params=None):
    """Executes a SigV4-signed JSON-RPC call to the Agent Registry MCP Endpoint."""
    url = f"{endpoint}/registry/{registry_id}/mcp"
    payload = {"jsonrpc": "2.0", "method": method}

    if not method.startswith("notifications/"):
        payload["id"] = next(_ids)
    if params is not None:
        payload["params"] = params

    body = json.dumps(payload).encode()
    signed = AWSRequest(method="POST", url=url, data=body,
                        headers={"Content-Type": "application/json"})
    SigV4Auth(creds, SERVICE, region).add_auth(signed)

    resp = requests.post(url, data=body, headers=dict(signed.headers), timeout=30)
    resp.raise_for_status()
    return resp.json() if resp.content else None


def invoke_agent_via_boto3(agent_runtime_arn, message, runtime_client):
    """Invokes the Bedrock AgentCore Runtime directly using standard Boto3."""
    payload = {
        "input": {"text": message}
    }

    try:
        response = runtime_client.invoke_agent_runtime(
            agentRuntimeArn=agent_runtime_arn,
            payload=json.dumps(payload).encode("utf-8"),
            contentType="application/json"
        )

        if "response" in response:
            body = response["response"]
            data = body.read() if hasattr(body, "read") else body
            if isinstance(data, bytes):
                data = data.decode("utf-8")

            try:
                parsed = json.loads(data)
                # Unpack common text fields from structural response variations
                for key in ["completion", "output", "result", "response", "text", "message"]:
                    if key in parsed:
                        return parsed[key]
                return parsed
            except json.JSONDecodeError:
                return data
        return None

    except Exception as e:
        print(f"Boto3 Invocation Error: {e}")
        return None


def tool_payload(result):
    """Safely handles content text extraction for tool returns."""
    content = (result or {}).get("content") or []
    if not content:
        return None
    
    # Check if content returned is a list or standard object wrapper
    if isinstance(content, list) and len(content) > 0:
        text = content[0].get("text", "")
    elif isinstance(content, dict):
        text = content.get("text", "")
    else:
        text = content
        
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return text


def main():
    # Gather ambient credentials
    session = boto3.Session()
    creds = session.get_credentials().get_frozen_credentials()

    # Define dedicated clients for the control plane and data plane
    control_client = boto3.client("agent-registry-control", region_name=REGION)
    runtime_client = boto3.client("bedrock-agentcore", region_name=REGION)

    # -----------------------------------------------------------------------
    # 1. Control Plane Discovery
    # -----------------------------------------------------------------------
    print("\n=== Available Registries ===")
    registries = control_client.list_registries()

    if not registries["registries"]:
        raise RuntimeError("No registries found.")

    for idx, r in enumerate(registries["registries"], start=1):
        print(f"{idx}. {r['name']}  ({r['registryArn']})")

    choice = int(input("\nSelect a registry by number: "))
    selected = registries["registries"][choice - 1]

    registry_id = selected["registryArn"].split("/")[-1]
    endpoint = f"https://agent-registry.{REGION}.api.aws"

    # -----------------------------------------------------------------------
    # 2. MCP Handshake Initialization
    # -----------------------------------------------------------------------
    mcp_call(endpoint, REGION, creds, registry_id, "initialize", {
        "protocolVersion": MCP_PROTOCOL_VERSION,
        "capabilities": {},
        "clientInfo": {"name": "demo-client", "version": "1.0"},
    })
    mcp_call(endpoint, REGION, creds, registry_id, "notifications/initialized")

    # -----------------------------------------------------------------------
    # 3. Dynamic Unfiltered Record Searching
    # -----------------------------------------------------------------------
    search_query = input("\nEnter search query: ")

    called = mcp_call(endpoint, REGION, creds, registry_id, "tools/call", {
        "name": "search_discoverable_registry_records",
        "arguments": {
            "searchQuery": search_query,
            "maxResults": 10,
        },
    })

    records = tool_payload(called.get("result", {}))
    if not records:
        print("No matching records found.")
        return

    # -----------------------------------------------------------------------
    # 4. Interactive Human Filtering Selection Menu
    # -----------------------------------------------------------------------
    print("\n=== Found Agents ===")
    agent_records = []
    for r in records:
        if r.get("recordType") == "AGENT" and r.get("descriptors", {}).get("a2aAgentCard"):
            agent_records.append(r)
            print(f"{len(agent_records)}. {r['name']} (ID: {r['recordId']})")

    if not agent_records:
        print("No agent records with an A2A Agent Card were found.")
        return

    agent_choice = int(input("\nSelect an agent to invoke by number: ")) - 1
    target_agent = agent_records[agent_choice]
    
    # Safely unpack the inner string representation of the A2A config card
    card_string = target_agent["descriptors"]["a2aAgentCard"]["data"]
    card_data = json.loads(card_string)
    agent_runtime_arn = card_data.get("url", "")
    
    if not agent_runtime_arn:
        print(f"Error: No operational runtime URL found inside the A2A card for {target_agent['name']}.")
        return

    # -----------------------------------------------------------------------
    # 5. Direct Execution Prompter
    # -----------------------------------------------------------------------
    human_prompt = input("\nEnter prompt for the agent: ")

    print(f"\n=== Invoking Agent Core Runtime via Boto3: {target_agent['name']} ===")
    print(f"Target ARN: {agent_runtime_arn}")
    
    agent_response = invoke_agent_via_boto3(agent_runtime_arn, human_prompt, runtime_client)
    
    print("\n=== Agent Response ===")
    if isinstance(agent_response, (dict, list)):
        print(json.dumps(agent_response, indent=2))
    else:
        print(agent_response)


if __name__ == "__main__":
    main()
