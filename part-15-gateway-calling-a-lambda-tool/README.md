# Part 15 — Gateway Calling a Lambda Tool

**AgentCore capability:** Gateway

First Gateway lab: turns a plain Lambda function (`code/mylambdatool.py`) into an MCP-compatible tool behind an AgentCore Gateway, described by an inline schema (`code/gatewayinlineschema.json`). `code/listtools.py` and `code/calltool.py` are small MCP JSON-RPC clients that list and invoke the tool over HTTP with an OAuth bearer token fetched by `code/getauthtoken.py`.

## Prerequisites

- A Lambda function deployed from `code/mylambdatool.py`
- An AgentCore Gateway with the inline schema attached and an OAuth authorizer (e.g. Cognito) configured

## Run it

1. Deploy the Lambda and create the Gateway per `commands/AllCommands.txt`
2. `python code/getauthtoken.py` to fetch a token
3. `python code/listtools.py` then `python code/calltool.py` to exercise the tool

---

[← Back to the lab index](../README.md)
