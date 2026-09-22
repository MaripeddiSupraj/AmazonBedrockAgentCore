# myagent.py
import json
import logging

from bedrock_agentcore import BedrockAgentCoreApp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AgentCore wraps this Python application and exposes the decorated entrypoint.
app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload):
    """
    Minimal Runtime-only example.

    There is deliberately:
    - no LLM call,
    - no AgentCore Memory,
    - no Gateway/tool call.

    The goal is to prove the Runtime request/response path first.
    """
    if isinstance(payload, (bytes, str)):
        try:
            payload = json.loads(payload)
        except Exception:
            payload = {}

    prompt = payload.get("prompt") or payload.get("input") or ""
    logger.info("Received prompt: %s", prompt)

    if not prompt:
        return {"message": "No prompt provided."}

    normalized = prompt.strip().lower()

    if normalized == "health":
        reply = "Agent application is running."
    elif "joke" in normalized:
        reply = "Why did the developer go broke? Because he used up all his cache."
    else:
        # Echo behavior makes it obvious that no model reasoning is happening.
        reply = f"You said: {prompt}"

    logger.info("Replying: %s", reply)
    return {"message": reply}


if __name__ == "__main__":
    app.run()
