# Part 17 — Calling an AgentCore Docker Agent from a Python Client

**AgentCore capability:** Runtime

A thin boto3 client (`client/client.py`) that invokes a Dockerized AgentCore Runtime agent and correctly reads back a streaming response body — useful as a template for any external service that needs to call your deployed agent.

## Prerequisites

- A deployed Docker-based agent runtime ARN (e.g. from Part 16)

## Run it

1. Set `agentRuntimeArn` in `client/client.py`
2. `python client/client.py`

---

[← Back to the lab index](../README.md)
