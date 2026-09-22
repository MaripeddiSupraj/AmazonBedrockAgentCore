# Part 08 — Deploy a Short-Term Memory Agent

**AgentCore capability:** Memory

First lab to use the real AgentCore Memory service. `mystmagent.py` calls `MemoryClient.create_event()` to persist each turn under a memory/session ID, giving the agent genuine short-term (session-scoped) recall instead of the in-process dict from Part 5.

## Prerequisites

- An AgentCore Memory resource created in your account (`MEMORY_ID`)
- IAM permissions for `bedrock-agentcore:CreateEvent` / `RetrieveMemories` (see `policies/`)

## Run it

1. `cd agent && pip install -r requirements.txt`
2. Set `MEMORY_ID` to your own memory resource
3. Deploy via `commands/AllCommands.txt` and chat with it across turns in the same session

---

[← Back to the lab index](../README.md)
