# Part 13 — Long-Term Memory with the Built-In Episodic Strategy

**AgentCore capability:** Memory

Demonstrates AgentCore's Episodic memory strategy, which stores two related namespaces per actor: individual episodes (session-scoped) and reflections (actor-scoped summaries across episodes). `agent/myepiagent.py` is the agent; `prompts/Prompts.txt` has example conversations designed to actually trigger episodic memory formation; `utils/ltmreadutil.py` reads both namespaces back out.

## Prerequisites

- An AgentCore Memory resource with the Episodic strategy enabled

## Run it

1. Deploy `agent/myepiagent.py`
2. Run through the example prompts in `prompts/Prompts.txt`
3. `python utils/ltmreadutil.py` to inspect episodes vs. reflections

---

[← Back to the lab index](../README.md)
