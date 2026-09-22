# AgentCore Course — Days 1–5 Reference Design

This folder is the **teaching reference** for the rest of this repository.

The older `part-NN-*` folders remain useful historical and feature labs. The first five days here are intentionally redesigned around the **current AgentCore CLI and current AWS mental model** so a learner understands the platform before they encounter larger examples.

## The five-day progression

| Day | New concept | What we deliberately leave out |
|---|---|---|
| **1** | AgentCore Runtime + entrypoint + deploy/invoke flow | LLM, Memory, tools |
| **2** | Runtime calling an Amazon Bedrock model | Memory, tools |
| **3** | Runtime sessions + isolated ephemeral state | AgentCore Memory |
| **4** | Programmatic client + `runtimeSessionId` | durable memory |
| **5** | AgentCore short-term Memory | long-term strategies |

The learning sequence is deliberate:

```text
Day 1
Python app
  -> AgentCore Runtime

Day 2
Python app
  -> AgentCore Runtime
  -> Bedrock model

Day 3
Client session ID
  -> dedicated Runtime session / microVM
  -> ephemeral state

Day 4
Your own Python client
  -> InvokeAgentRuntime
  -> runtimeSessionId
  -> Runtime

Day 5
Runtime
  -> AgentCore Memory
  -> durable short-term events
```

## Why this format is different

Every day uses the same teaching loop:

```text
1. Story
2. Mental model
3. Architecture
4. Minimal code
5. Predict the result
6. Run it
7. Observe the result
8. Break one assumption
9. Change the code
10. Explain it back
11. Production gap
```

A learner is **not finished** because a command worked.

A learner is finished when they can:

- explain the component without code,
- draw the request flow,
- predict behavior before running,
- prove the behavior with evidence,
- change one thing themselves,
- explain what would be different in production.

## Current CLI used by this reference

Install:

```bash
npm install -g @aws/agentcore
agentcore --help
```

Create a learning project:

```bash
agentcore create --name Day01Runtime --framework Strands --model-provider Bedrock --memory none --build CodeZip --protocol HTTP
```

The generated project places the agent entrypoint under:

```text
app/<AgentName>/main.py
```

For each day, copy that day's `main.py` into the generated agent's `main.py` and add any listed Python dependencies.

Then use:

```bash
agentcore dev
agentcore deploy
agentcore invoke "your prompt"
```

Where a day needs session continuity, the README shows `--session-id` or the AWS SDK equivalent.

> The scaffold may include framework dependencies even when a learning example uses plain `BedrockAgentCoreApp`. That is intentional: Days 1–5 isolate AgentCore concepts before introducing agent-framework abstractions.

## Relationship to the existing labs

| Course day | Existing lab that expands it |
|---|---|
| Day 1 | Part 03 |
| Day 2 | Part 04 |
| Day 3 | Part 05 |
| Day 4 | Part 06 |
| Day 5 | Part 08 |

Start with this course. Use the corresponding `part-*` folder afterward as an additional implementation/history reference.

## For contributors and coding agents

Before authoring Day 6 onward, read [TEACHING_STANDARD.md](TEACHING_STANDARD.md).

Do **not** continue the course by merely creating:

```text
Prerequisites
Run these commands
Done
```

The course is explanation-first and evidence-driven.
