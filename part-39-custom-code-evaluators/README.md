# Part 39 — Custom Code Evaluators

**AgentCore capability:** Evaluations

Goes beyond model-as-judge with deterministic, code-based evaluators: two Lambda functions (`evaluators/FinalAnswerEvaluator.py`, `evaluators/LatencyEvaluator.py`) that AgentCore Evaluations invokes directly to score correctness and latency against the Part 36 agent.

## Prerequisites

- The two evaluator Lambdas deployed with their resource policies (`policies/`)

## Run it

1. Deploy the evaluator Lambdas
2. `bash agent/deploy.sh`, deploy the agent as a Runtime agent
3. Register the Lambda evaluators in AgentCore Evaluations and run an evaluation job

---

[← Back to the lab index](../README.md)
