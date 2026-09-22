# Part 48 — HITL Agent Execution After Registry Discovery

**AgentCore capability:** Registry + Runtime

The capstone lab: discovers an agent via the Registry (`discovery/awssdk.py` / `discovery/mcp.py`, using the `registry-record/AgentCard.json` record), then invokes it through AgentCore Runtime with a human-in-the-loop confirmation step before the action executes.

## Prerequisites

- An agent published to the Registry with an AgentCard
- A deployed Runtime agent to invoke

## Run it

1. `bash setup/setup.sh`
2. `python discovery/awssdk.py` (or `discovery/mcp.py`) to discover the agent
3. Approve the human-in-the-loop prompt when asked, and confirm the agent executes

---

[← Back to the lab index](../README.md)
