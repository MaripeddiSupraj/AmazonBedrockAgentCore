# Part 03 — Deploy a Simple Agent with the Starter Toolkit

**AgentCore capability:** Runtime

The "hello world" of AgentCore: a minimal Python agent (`myagent.py`) that echoes back whatever prompt it receives, wired up with the `@app.entrypoint` decorator from the `bedrock-agentcore` SDK and deployed with the classic Python starter toolkit (`bedrock-agentcore-starter-toolkit`, `agentcore configure` / `agentcore launch` / `agentcore invoke`).

## Prerequisites

- AWS account with Bedrock AgentCore enabled in your region
- IAM execution role + trust policy (see `policies/`) attached to your AWS user
- Python 3.11+, `pip install bedrock-agentcore-starter-toolkit boto3`

## Run it

1. `cd agent && pip install -r requirements.txt`
2. Follow the commands in `commands/AllCommands.txt` to configure and launch the agent
3. `agentcore invoke '{"prompt": "tell me a joke"}'`

> **Note:** Uses the original Python starter-toolkit CLI, not the newer preview `agentcore` npm CLI covered in Part 44.

---

[← Back to the lab index](../README.md)
