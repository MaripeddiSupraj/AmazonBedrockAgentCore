import json
import os
import uuid

import boto3

REGION = os.getenv("AWS_REGION", "us-west-2")
AGENT_RUNTIME_ARN = os.getenv("AGENT_RUNTIME_ARN", "")

client = boto3.client("bedrock-agentcore", region_name=REGION)


def new_session_id(label: str = "course") -> str:
    """Create a readable session ID long enough for Runtime use."""
    return f"{label}-{uuid.uuid4().hex}"


def invoke_agent(prompt: str, session_id: str) -> dict:
    """Invoke the deployed Runtime using session metadata + a JSON payload."""
    if not AGENT_RUNTIME_ARN:
        raise RuntimeError("Set AGENT_RUNTIME_ARN before running the client.")

    payload = json.dumps({"prompt": prompt}).encode("utf-8")

    response = client.invoke_agent_runtime(
        agentRuntimeArn=AGENT_RUNTIME_ARN,
        runtimeSessionId=session_id,
        payload=payload,
        qualifier="DEFAULT",
    )

    raw_body = response["response"].read()
    result = json.loads(raw_body)

    return {
        "runtime_session_id": response.get("runtimeSessionId", session_id),
        "agent_response": result,
    }


def main():
    session_id = new_session_id("day04")
    print("AgentCore Day 4 client")
    print(f"Session: {session_id}")
    print("Commands: /id, /new, /quit")

    while True:
        prompt = input("You: ").strip()

        if not prompt:
            continue

        if prompt == "/quit":
            break

        if prompt == "/id":
            print(f"Current session: {session_id}")
            continue

        if prompt == "/new":
            session_id = new_session_id("day04")
            print(f"New session: {session_id}")
            continue

        try:
            result = invoke_agent(prompt, session_id)
            print(json.dumps(result, indent=2))
        except Exception as exc:
            print(f"Invocation failed: {exc}")


if __name__ == "__main__":
    main()
