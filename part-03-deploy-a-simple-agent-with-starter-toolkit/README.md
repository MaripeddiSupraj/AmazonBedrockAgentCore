# Part 03 — Deploy a Simple Agent with the Starter Toolkit

**AgentCore capability:** Runtime

This is the best place to learn the **Runtime** mental model because this agent deliberately has **no LLM, no AgentCore Memory, no Gateway, and no tools**.

The purpose is to answer one question first:

> What exactly does AgentCore Runtime do for a plain Python agent application?

> **CLI note:** This lab was written for the older Python `bedrock-agentcore-starter-toolkit` flow (`configure / launch / invoke`). AWS now recommends the current `@aws/agentcore` CLI for new projects. Learn the Runtime concept here; do not treat `launch` as the current command to memorize.

---

## 1. What you will learn

By the end of this lab you should be able to explain:

- what `BedrockAgentCoreApp` does,
- what `@app.entrypoint` means,
- how an invocation payload reaches your Python function,
- what AgentCore Runtime is responsible for,
- what AgentCore Runtime is **not** doing in this example,
- why this agent cannot truly remember a previous conversation.

---

## 2. Theory — Runtime without AI magic

It is easy to think:

```text
AgentCore Runtime = LLM
```

That is incorrect.

Runtime is the **managed execution environment** that hosts your agent application.

Your application can contain:

- simple deterministic Python,
- a Bedrock model call,
- Strands/LangGraph/ADK/OpenAI Agents code,
- Gateway calls,
- Memory calls,
- Browser/Code Interpreter calls,
- or combinations of those.

Part 03 intentionally starts with deterministic Python so you can see the platform boundary clearly.

---

## 3. Request flow

When you invoke this lab:

```text
agentcore invoke
      |
      | {"prompt": "hello"}
      v
AgentCore Runtime
      |
      v
BedrockAgentCoreApp
      |
      v
@app.entrypoint
invoke(payload)
      |
      v
normal Python code
      |
      v
{"message": "You said: hello"}
      |
      v
caller
```

There is **no model call** between the entrypoint and the response.

---

## 4. Read the code before running

Open:

```text
agent/myagent.py
```

Focus on three pieces.

### A. Application object

```python
app = BedrockAgentCoreApp()
```

This creates the AgentCore application wrapper.

### B. Entrypoint

```python
@app.entrypoint
def invoke(payload):
```

This marks the function AgentCore should call for an invocation.

### C. Deterministic behavior

The code handles:

- `health`
- prompts containing `joke`
- all other prompts as an echo

That is important because the output proves Python executed, not that an LLM reasoned.

---

## 5. What this lab does NOT have

| Feature | Present? | Why |
|---|---:|---|
| AgentCore Runtime | Yes | this is the concept being learned |
| Foundation model | No | introduced next |
| AgentCore Memory | No | introduced later |
| Gateway | No | introduced later |
| OAuth / Identity | No | introduced later |
| Browser / Code Interpreter | No | introduced later |

If you ask this lab:

```text
My name is Alex.
```

and later:

```text
What is my name?
```

you should **not** interpret any answer as durable memory. This application has not implemented memory.

---

## 6. Prerequisites

- AWS sandbox/development account
- a supported Region for AgentCore Runtime
- Python
- AWS credentials with permissions required by the lab
- the educational IAM examples under `policies/`

Before deploying:

```bash
aws sts get-caller-identity
```

Confirm you are using the intended account.

---

## 7. Run it

The complete legacy-lab setup is in:

```text
commands/AllCommands.txt
```

High-level sequence:

```bash
cd agent
pip install -r requirements.txt

agentcore configure -e myagent.py
agentcore launch

agentcore invoke '{"prompt": "hello AgentCore"}'
agentcore invoke '{"prompt": "health"}'
agentcore invoke '{"prompt": "tell me a joke"}'
```

Again, `configure/launch` is the historical Starter Toolkit workflow used by this lab.

---

## 8. Expected results

For:

```json
{"prompt": "hello AgentCore"}
```

expect the application to echo the prompt.

For:

```json
{"prompt": "health"}
```

expect:

```text
Agent application is running.
```

For a joke prompt, expect the fixed joke in the Python source.

If the response changes creatively between invocations, stop and investigate: this lab is supposed to be deterministic.

---

## 9. Learner assignment

### Task

Add a new deterministic command:

```text
version
```

that returns something like:

```json
{"message": "part-03-v1"}
```

Then redeploy and invoke it.

### Why this task matters

It proves you understand:

```text
source change
  -> deployment/update
  -> Runtime
  -> invocation
  -> new application behavior
```

instead of only copying the original commands.

---

## 10. Success criteria

You have completed Part 03 only when you can explain all four:

1. **Runtime hosts the application.**
2. **The entrypoint receives the invocation payload.**
3. **No LLM is used in this lab.**
4. **No durable memory exists in this lab.**

You should also be able to draw:

```text
CLI -> Runtime -> @app.entrypoint -> Python -> response
```

without looking at this README.

---

## 11. Common confusion

### "The agent answered, so did Bedrock generate the answer?"

No. Not in this lab. The Python code generates the response.

### "Does Runtime automatically remember my previous prompt?"

Do not rely on in-process/runtime state as durable conversational memory. AgentCore Memory is a separate capability introduced later.

### "Should I use `agentcore launch` for a brand-new project?"

Use the current AgentCore CLI/docs for new projects. `launch` is preserved here because this lab demonstrates an older Starter Toolkit generation.

---

## 12. Production note

This is deliberately not a production application. It exists to isolate the Runtime concept before introducing models, state, tools, identity, and governance.

---

[← Back to the lab index](../README.md) · [Learning guide](../LEARNING_GUIDE.md)
