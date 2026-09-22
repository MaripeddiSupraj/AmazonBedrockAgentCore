# Part 16 — Docker-Based Agent with OAuth Gateway & Lambda Tool

**AgentCore capability:** Runtime + Gateway

Wraps Part 15 end-to-end: a Dockerized Flask agent (`agent/app.py`) that authenticates to the Gateway with an OAuth token and calls the Lambda tool through it, built with a proper multi-stage-friendly `Dockerfile` (non-root user, healthcheck) and pushed to ECR with `agent/deploy.sh`.

## Prerequisites

- Docker installed
- The Gateway + Lambda tool from Part 15 already deployed
- An ECR repository (created by `deploy.sh` if it doesn't exist)

## Run it

1. Fill in `ACCOUNT_ID` / `REGION` placeholders in `agent/deploy.sh`
2. `bash agent/deploy.sh` to build and push the image
3. Deploy the pushed image as an AgentCore Runtime per `commands/Agent Commands.txt`

---

[← Back to the lab index](../README.md)
