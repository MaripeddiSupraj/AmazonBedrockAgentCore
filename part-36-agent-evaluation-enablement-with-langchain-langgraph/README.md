# Part 36 — Agent Evaluation Enablement with LangChain + LangGraph

**AgentCore capability:** Evaluations + Observability

Rebuilds the agent as a LangGraph state machine and turns on LangChain OpenTelemetry instrumentation (`LangchainInstrumentor().instrument()`), which is the prerequisite for AgentCore Evaluations to be able to score its runs.

## Prerequisites

- ADOT/observability configured so evaluation traces are captured

## Run it

1. `bash agent/deploy.sh`, deploy as a Runtime agent
2. Run some conversations, then enable Evaluations on the agent in the console

---

[← Back to the lab index](../README.md)
