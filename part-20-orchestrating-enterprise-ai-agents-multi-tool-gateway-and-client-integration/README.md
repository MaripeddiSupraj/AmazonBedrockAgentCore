# Part 20 — Orchestrating Enterprise AI Agents: Multi-Tool Gateway and Client Integration

**AgentCore capability:** Runtime + Gateway

Picks up where Part 19 left off: an LLM-driven agent (`agent/app.py`) now orchestrates the three-tool Gateway itself — resolving a city, fetching its weather, and posting a summary to Slack — in response to a single natural-language request, with `client/client.py` as the external caller. See `arch diagram.jpg` for the full request path.

## Prerequisites

- The Part 19 multi-tool Gateway deployed and reachable

## Run it

1. `bash setup/Pythonsetup.sh && bash setup/Envsetup.sh`
2. `bash agent/deploy.sh`, deploy as a Runtime agent
3. `python client/client.py` and try: "Get the coordinates for Berlin and send them to #social"

---

[← Back to the lab index](../README.md)
