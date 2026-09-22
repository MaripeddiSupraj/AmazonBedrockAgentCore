# Part 30 — From Insights to Visibility: Monitoring Your Market Intelligence Agent with ADOT

**AgentCore capability:** Observability

Takes the Part 26 Browser-tool agent and instruments it with the AWS Distro for OpenTelemetry (ADOT), adding trace spans and baggage/context propagation so every step of a research request shows up in AgentCore Observability.

## Prerequisites

- ADOT Docker wrapper / observability configured per the AWS docs

## Run it

1. `bash setup/Pythonsetup.sh && bash setup/Envsetup.sh`
2. `bash agent/deploy.sh`, deploy as a Runtime agent
3. Run a few requests, then check traces in the AgentCore Observability console

---

[← Back to the lab index](../README.md)
