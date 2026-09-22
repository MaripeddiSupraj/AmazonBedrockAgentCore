import os

from bedrock_agentcore import BedrockAgentCoreApp
from bedrock_agentcore.memory import MemoryClient

app = BedrockAgentCoreApp()

REGION = os.getenv("AWS_REGION", "us-west-2")
MEMORY_ID = os.getenv("MEMORY_ID", "")

memory = MemoryClient(region_name=REGION)


def read_history(actor_id: str, memory_session_id: str) -> list[dict]:
    events = memory.list_events(
        memory_id=MEMORY_ID,
        actor_id=actor_id,
        session_id=memory_session_id,
        include_payload=True,
        max_results=100,
    )

    history = []

    for event in events:
        for item in event.get("payload", []):
            conversational = item.get("conversational")
            if not conversational:
                continue

            history.append(
                {
                    "role": conversational.get("role"),
                    "text": conversational.get("content", {}).get("text", ""),
                    "event_id": event.get("eventId"),
                }
            )

    return history


@app.entrypoint
def handler(request):
    """Day 5: persist short-term events outside the Runtime microVM."""
    if not MEMORY_ID:
        return {
            "ok": False,
            "message": "MEMORY_ID is not configured.",
        }

    prompt = request.get("prompt")
    actor_id = request.get("actor_id", "learner-001")
    memory_session_id = request.get("memory_session_id", "day05-memory-session")

    if not isinstance(prompt, str) or not prompt.strip():
        return {"ok": False, "message": "Send a non-empty 'prompt' string."}

    prompt = prompt.strip()

    if prompt == "/history":
        history = read_history(actor_id, memory_session_id)
        return {
            "ok": True,
            "actor_id": actor_id,
            "memory_session_id": memory_session_id,
            "history": history,
        }

    event = memory.create_event(
        memory_id=MEMORY_ID,
        actor_id=actor_id,
        session_id=memory_session_id,
        messages=[(prompt, "USER")],
        extraction_mode="SKIP",
    )

    return {
        "ok": True,
        "stored": prompt,
        "event_id": event.get("eventId"),
        "actor_id": actor_id,
        "memory_session_id": memory_session_id,
        "state_type": "agentcore-short-term-memory",
    }


if __name__ == "__main__":
    app.run()
