# Part 06 — Create a Python Client to Chat with an Ephemeral Agent

**AgentCore capability:** Runtime

A small interactive CLI chat client (`mychatclient.py`) that calls `bedrock-agentcore`'s `invoke_agent_runtime` directly via boto3, generating a stable `runtimeSessionId` per run so the Part 5 agent keeps context for the length of the chat.

## Prerequisites

- A deployed agent runtime ARN from Part 5 (or any other lab)

## Run it

1. Edit `AGENT_RUNTIME_ARN` in `client/mychatclient.py`
2. `python client/mychatclient.py`
3. Type messages; type `exit` to quit

---

[← Back to the lab index](../README.md)
