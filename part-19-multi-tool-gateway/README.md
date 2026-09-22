# Part 19 — Multi-Tool Gateway

**AgentCore capability:** Gateway

Extends the single-tool Gateway pattern to three tools behind one Gateway: a weather Lambda, a LocationIQ geocoding tool (`schemas/locationIQschema.json`), and a Slack notifier. `client/testclient.py` fetches an OAuth token and calls each tool directly to confirm the Gateway is wired correctly before an agent ever touches it.

## Prerequisites

- A LocationIQ API key
- A Slack webhook/app for the notifier tool
- Cognito (or your chosen IdP) client credentials for the Gateway

## Run it

1. `bash setup/Envsetup.sh`
2. Fill in the REPLACE placeholders in `client/testclient.py`
3. `python client/testclient.py` to list and call each tool

---

[← Back to the lab index](../README.md)
