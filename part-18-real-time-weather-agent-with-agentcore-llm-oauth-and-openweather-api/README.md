# Part 18 — Real-Time Weather Agent with AgentCore, LLM, OAuth and OpenWeather API

**AgentCore capability:** Runtime + Gateway + Identity

A complete, product-shaped example (see `Arch Diagram.jpg`): the agent uses an LLM to decide whether a message needs live weather data, discovers the weather tool dynamically from the Gateway at runtime (no hardcoded tool names), and fetches OAuth client-credentials from AWS Secrets Manager rather than hardcoding them. The Lambda tool calls the OpenWeather free-tier API.

## Prerequisites

- A free OpenWeather API key (test it with `utils/TestOpenAPIKey.txt`)
- A Secrets Manager secret holding your OAuth `CLIENT_ID` / `CLIENT_SECRET` / `TOKEN_URL` / `SCOPE`
- The Gateway + Lambda tool pattern from Parts 15–16

## Run it

1. Read `Scenario.txt` for the full brief
2. Set up the secret and Gateway per `setup/Envsetup.sh`
3. `bash agent/deploy.sh` to build/push, then deploy as a Runtime agent

---

[← Back to the lab index](../README.md)
