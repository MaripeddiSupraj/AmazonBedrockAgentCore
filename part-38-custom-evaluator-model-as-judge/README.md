# Part 38 — Custom Evaluator: Model-as-Judge

**AgentCore capability:** Evaluations

Configuration-only lab: defines a custom "QA Auditor" model-as-judge evaluator in two variants (with and without tool-use awareness) plus its IAM configuration policy — no app code, just the evaluator prompt/config you register with AgentCore Evaluations.

## Prerequisites

- An agent already emitting evaluation traces (e.g. from Part 36)

## Run it

1. Review `CustomEvaluator QAAuditorwithouttooluse.txt` and `...withtooluse.txt`
2. Register the evaluator using `EvalConfigurationPolicy.txt` as the IAM baseline
3. Test with the prompts in `SampleInputs.txt`

---

[← Back to the lab index](../README.md)
