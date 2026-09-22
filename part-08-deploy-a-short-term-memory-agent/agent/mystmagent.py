import json
import logging
import os

import boto3
from bedrock_agentcore import BedrockAgentCoreApp
from bedrock_agentcore.memory import MemoryClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REGION = os.getenv("AWS_REGION", "us-east-1")
MEMORY_ID = os.getenv("MEMORY_ID", "")
MODEL_ID = os.getenv("MODEL_ID", "")

app = BedrockAgentCoreApp()
bedrock = boto3.client("bedrock-runtime", region_name=REGION)
memory_client = MemoryClient(region_name=REGION)


def store_message(actor_id: str, session_id: str, text: str, role: str):
    """
    Store one conversational message.

    Important mental model:
      actor_id  = the entity/user the memory belongs to
      session_id = the logical conversation/session
      role      = USER or ASSISTANT inside that conversation

    Do not use USER/ASSISTANT as actor IDs.
    """
    event = memory_client.create_event(
        memory_id=MEMORY_ID,
        actor_id=actor_id,
        session_id=session_id,
        messages=[(text, role)],
    )
    logger.info(
        "Stored %s event for actor=%s session=%s event=%s",
        role,
        actor_id,
        session_id,
        event.get("eventId", "unknown"),
    )
    return event


def load_conversation(actor_id: str, session_id: str):
    """Read the conversation history for one actor + session."""
    events = memory_client.list_events(
        memory_id=MEMORY_ID,
        actor_id=actor_id,
        session_id=session_id,
        include_payload=True,
        max_results=50,
    )

    messages = []
    for event in events:
        for payload_item in event.get("payload", []):
            conversational = payload_item.get("conversational")
            if not conversational:
                continue

            role = conversational.get("role", "").lower()
            text = conversational.get("content", {}).get("text", "")

            if role in {"user", "assistant"} and text:
                messages.append({"role": role, "content": text})

    return messages


def reset_memory(actor_id: str, session_id: str):
    """Delete the events belonging only to this actor + session."""
    events = memory_client.list_events(
        memory_id=MEMORY_ID,
        actor_id=actor_id,
        session_id=session_id,
        include_payload=False,
        max_results=100,
    )

    for event in events:
        memory_client.delete_event(
            memory_id=MEMORY_ID,
            actor_id=actor_id,
            session_id=session_id,
            event_id=event["eventId"],
        )

    logger.info("Memory reset for actor=%s session=%s", actor_id, session_id)


def extract_assistant_text(result: dict) -> str:
    """Extract text blocks from an Anthropic Messages API response."""
    blocks = result.get("content", [])
    text_parts = [
        block.get("text", "")
        for block in blocks
        if isinstance(block, dict) and block.get("type") == "text"
    ]
    return "\n".join(part for part in text_parts if part).strip()


@app.entrypoint
def invoke(payload):
    if isinstance(payload, (bytes, str)):
        try:
            payload = json.loads(payload)
        except Exception:
            payload = {}

    if not MEMORY_ID:
        return {
            "message": (
                "MEMORY_ID is not configured. Set it to your AgentCore Memory resource ID."
            )
        }

    if not MODEL_ID:
        return {
            "message": (
                "MODEL_ID is not configured. Set it to a Bedrock Claude model ID "
                "available in your account/region."
            )
        }

    user_input = payload.get("prompt") or payload.get("input") or ""
    actor_id = payload.get("actor_id") or "demo-user"
    memory_session_id = payload.get("memory_session_id") or "demo-session"

    if not user_input:
        return {"message": "No prompt provided."}

    if user_input.strip().lower() == "reset":
        reset_memory(actor_id, memory_session_id)
        return {
            "message": (
                f"Memory reset for actor={actor_id}, session={memory_session_id}."
            )
        }

    # 1. Persist the current user turn.
    store_message(actor_id, memory_session_id, user_input, "USER")

    # 2. Rebuild conversation history from AgentCore Memory.
    messages = load_conversation(actor_id, memory_session_id)

    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "system": (
            "You are a helpful assistant. Use the supplied conversation history "
            "to answer the latest user message."
        ),
        "messages": messages,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9,
    }

    try:
        # 3. Ask the model using the conversation reconstructed from Memory.
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(request_body).encode("utf-8"),
            contentType="application/json",
            accept="application/json",
        )

        result = json.loads(response["body"].read())
        assistant_text = extract_assistant_text(result)

        if not assistant_text:
            assistant_text = "The model returned no text response."

        # 4. Persist the assistant turn under the SAME actor + session.
        store_message(
            actor_id,
            memory_session_id,
            assistant_text,
            "ASSISTANT",
        )

        return {
            "message": assistant_text,
            "actor_id": actor_id,
            "memory_session_id": memory_session_id,
        }

    except Exception as exc:
        logger.exception("Error calling Bedrock")
        return {"message": f"Error calling Bedrock: {exc}"}


if __name__ == "__main__":
    app.run()
