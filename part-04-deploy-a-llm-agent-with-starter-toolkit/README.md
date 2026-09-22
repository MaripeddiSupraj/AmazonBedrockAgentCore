# Part 04 — Deploy an LLM Agent with the Starter Toolkit

**AgentCore capability:** Runtime

Same deployment pattern as Part 3, but the entrypoint now calls a real foundation model (`myllmagent.py` invokes `bedrock-runtime` with Amazon Titan Text Lite) instead of canned string matching.

## Prerequisites

- Everything from Part 3
- Model access enabled for the target model ID in the Bedrock console

## Run it

1. `cd agent && pip install -r requirements.txt`
2. Configure/launch via `commands/AllCommands.txt`
3. Invoke with any prompt and confirm you get a real model completion back

> **Note:** Swap `MODEL_ID` for any model your account has access to.

---

[← Back to the lab index](../README.md)
