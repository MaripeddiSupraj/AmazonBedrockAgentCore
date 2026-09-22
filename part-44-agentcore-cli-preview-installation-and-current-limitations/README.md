# Part 44 — AgentCore CLI Preview: Installation and Current Limitations

**AgentCore capability:** Tooling

Covers the newer, npm-distributed `@aws/agentcore` CLI (`agentcore create / dev / deploy / invoke / add / logs`), which is a different, more scaffolding-oriented tool from the classic Python `bedrock-agentcore-starter-toolkit` used in Parts 3–20. `main.py` is a minimal handler-style agent used to exercise it, plus notes on what was still rough in preview at the time of writing.

## Prerequisites

- Node.js/npm
- `npm install -g @aws/agentcore`

## Run it

1. `agentcore --version` to confirm install
2. `agentcore create` to scaffold a project, or use `main.py` directly
3. `agentcore dev` to test locally, `agentcore deploy` to ship it

> **Note:** Check the current release notes before relying on this — the CLI was in preview when this lab was written and command names/flags can change: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html

---

[← Back to the lab index](../README.md)
