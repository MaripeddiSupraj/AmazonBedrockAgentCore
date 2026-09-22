import os

from bedrock_agentcore import BedrockAgentCoreApp
from bedrock_agentcore.memory import MemoryClient

app = BedrockAgentCoreApp()

REGION = os.getenv("AWS_REGION", "us-west-2")
memory = MemoryClient(region_name=REGION)


def resolve_memory_id() -> tuple[str, str]:
    """
    Prefer an explicit MEMORY_ID for manual/local experiments.

    When the current AgentCore CLI creates a managed Memory connection for an
    agent, it injects an environment variable named MEMORY_<RESOURCE_NAME>_ID.
    Discover that generated variable so this teaching example does not depend
    on a hardcoded resource name.
    """
    explicit = os.getenv("MEMORY_ID")
    if explicit:
        return explicit, "MEMORY_ID"

    generated = [
        (name, value)
        for name, value in os.environ.items()
        if name.startswith("MEMORY_") and name.endswith("_ID") and value
    ]

    if len(generated) == 1:
        return generated[0][1], generated[0][0]

    return "", ""


def read_history(memory_id: str, actor_id: str, memory_session_id: str) -> list[dict]:
    events = memory.list_events(
        memory_id=memory_id,
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
    memory_id, memory_env_var = resolve_memory_id()

    if not memory_id:
        return {
            "ok": False,
            "message": (
                "No Memory ID found. Use the CLI-managed short-term Memory "
                "connection or configure MEMORY_ID explicitly."
            ),
        }

    prompt = request.get("prompt")
    actor_id = request.get("actor_id", "learner-001")
    memory_session_id = request.get("memory_session_id", "day05-memory-session")

    if not isinstance(prompt, str) or not prompt.strip():
        return {"ok": False, "message": "Send a non-empty 'prompt' string."}

    prompt = prompt.strip()

    if prompt == "/history":
        return {
            "ok": True,
            "actor_id": actor_id,
            "memory_session_id": memory_session_id,
            "memory_env_var": memory_env_var,
            "history": read_history(memory_id, actor_id, memory_session_id),
        }

    event = memory.create_event(
        memory_id=memory_id,
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
        "memory_env_var": memory_env_var,
        "state_type": "agentcore-short-term-memory",
    }


if __name__ == "__main__":
    app.run()
