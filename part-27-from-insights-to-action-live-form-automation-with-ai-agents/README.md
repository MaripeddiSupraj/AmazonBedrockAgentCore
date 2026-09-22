# Part 27 — From Insights to Action: Live Form Automation with AI Agents

**AgentCore capability:** Browser (Playwright)

Goes from "research" to "act": using Playwright directly (async, headless), the agent parses a natural-language instruction, fills in a live HTML form (`agent/Employee.html`) with the extracted field values, and submits it — a pattern for agentic form-filling / RPA-style tasks.

## Prerequisites

- `playwright install` (browser binaries) inside the container/image

## Run it

1. `bash setup/Pythonsetup.sh && bash setup/Envsetup.sh`
2. `bash agent/deploy.sh`, deploy as a Runtime agent
3. Give it a form URL plus the values to fill in

---

[← Back to the lab index](../README.md)
