from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()


@app.entrypoint
def handler(request):
    """Day 1: prove the AgentCore Runtime request/response path."""
    prompt = request.get("prompt")

    if not isinstance(prompt, str) or not prompt.strip():
        return {
            "ok": False,
            "message": "Send a non-empty string in the 'prompt' field.",
        }

    prompt = prompt.strip()

    if prompt.lower() == "health":
        return {
            "ok": True,
            "message": "Runtime application is healthy.",
            "handled_by": "plain-python",
        }

    return {
        "ok": True,
        "message": f"Runtime received: {prompt}",
        "handled_by": "plain-python",
    }


if __name__ == "__main__":
    app.run()
