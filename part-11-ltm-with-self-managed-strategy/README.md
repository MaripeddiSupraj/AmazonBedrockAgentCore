# Part 11 — Long-Term Memory with a Self-Managed Strategy

**AgentCore capability:** Memory

Instead of relying on a built-in strategy, `myltmsmsagent.py` manages memory extraction itself and fans important events out to S3 (for durable storage) and SNS (for notification), giving you full control over what gets kept and where.

## Prerequisites

- An S3 bucket and SNS topic in your account
- IAM permissions for S3 `PutObject` and SNS `Publish` (see `policies/`)

## Run it

1. Set `S3_BUCKET` and `SNS_TOPIC_ARN` in `agent/myltmsmsagent.py` to your own resources
2. Deploy via `commands/AllCommands.txt`

---

[← Back to the lab index](../README.md)
