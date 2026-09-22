# Part 24 — Code Interpreter — Build an AI Agent That Writes and Executes Code

**AgentCore capability:** Code Interpreter

Introduces the AgentCore Code Interpreter sandbox: `agent/app.py` gives the model a `code_interpreter` tool it can call to write and run Python for math, data analysis, or plotting, with results returned straight into the conversation.

## Prerequisites

- Code Interpreter enabled for your AgentCore account/region

## Run it

1. `bash setup/Pythonsetup.sh && bash setup/Envsetup.sh`
2. `bash agent/deploy.sh`, deploy as a Runtime agent
3. Ask it a question that needs computation, e.g. "plot the first 10 Fibonacci numbers"

---

[← Back to the lab index](../README.md)
