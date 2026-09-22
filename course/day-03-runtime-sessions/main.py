from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

# IMPORTANT:
# For the default microVM Runtime model, each runtimeSessionId gets its own
# isolated execution environment. This process-local state therefore belongs
# only to the current Runtime session and disappears when that compute ends.
SESSION_STATE = {
    "turn": 0,
    "prompts": [],
}


@app.entrypoint
def handler(request):
    """Day 3: demonstrate ephemeral state inside one Runtime session."""
    prompt = request.get("prompt")

    if not isinstance(prompt, str) or not prompt.strip():
        return {"ok": False, "message": "Send a non-empty 'prompt' string."}

    prompt = prompt.strip()

    SESSION_STATE["turn"] += 1
    SESSION_STATE["prompts"].append(prompt)

    return {
        "ok": True,
        "turn": SESSION_STATE["turn"],
        "current_prompt": prompt,
        "prompts_seen_in_this_compute": list(SESSION_STATE["prompts"]),
        "state_type": "ephemeral-runtime-session-state",
    }


if __name__ == "__main__":
    app.run()
