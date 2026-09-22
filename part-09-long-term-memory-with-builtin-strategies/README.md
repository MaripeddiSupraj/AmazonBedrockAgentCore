# Part 09 — Long-Term Memory with Built-In Strategies

**AgentCore capability:** Memory

Moves from session memory to AgentCore's built-in long-term memory strategies (e.g. summarization). `mysltmagent.py` is the agent; `utils/ltmreadutil.py` is a standalone inspection script that discovers every active strategy on a Memory resource and dumps what's stored in each namespace — handy for debugging what the agent actually remembers.

## Prerequisites

- An AgentCore Memory resource with a built-in strategy (e.g. Summarization) enabled

## Run it

1. Deploy `agent/mysltmagent.py` via `commands/AllCommands.txt`
2. Have a multi-turn conversation with it
3. `python utils/ltmreadutil.py` to see what got summarized/stored

---

[← Back to the lab index](../README.md)
