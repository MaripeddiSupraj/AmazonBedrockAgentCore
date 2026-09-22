# Part 05 — Deploy an Ephemeral Memory Agent

**AgentCore capability:** Runtime

Shows the difference between "the agent remembers within one run" and "the agent remembers across sessions": `myagentwithsesmgmt.py` keeps conversation history in a plain in-process dict, so memory only survives as long as the container does. This is the baseline the later Memory-service labs (8, 9, 11, 13) build on.

## Prerequisites

- Everything from Part 3/4

## Run it

1. `cd agent && pip install -r requirements.txt`
2. Deploy via `commands/AllCommands.txt`
3. Chat with it using the Part 6 client to see memory reset on a fresh session

> **Note:** No AgentCore Memory resource needed here — this is intentionally the "before" example.

---

[← Back to the lab index](../README.md)
