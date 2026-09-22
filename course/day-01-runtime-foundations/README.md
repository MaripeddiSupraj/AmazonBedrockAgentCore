# Day 01 — AgentCore Runtime Foundations

## Today’s question

> What happens when my Python function runs inside Amazon Bedrock AgentCore Runtime?

Do **not** start with an LLM. First understand the platform that runs the code.

---

## Why should I care?

When an agent replies, several different systems may be involved:

- your client,
- AgentCore Runtime,
- your Python application,
- a foundation model,
- Memory,
- tools.

If you introduce all of them on Day 1, it becomes impossible to tell which layer is responsible for what.

Today we isolate just this:

```text
request -> Runtime -> Python -> response
```

---

## One-sentence mental model

> **AgentCore Runtime is the managed execution environment for your agent application; it does not automatically make ordinary Python code intelligent.**

---

## Build on yesterday

There is no previous day.

This is the base layer for everything else:

```text
                 TODAY
Client  ---------------------->  AgentCore Runtime
                                      |
                                      v
                                  Python code
                                      |
                                      v
                                   response
```

No model. No Memory. No Gateway.

---

## Architecture / request flow

```text
agentcore invoke "hello"
        |
        | invocation payload
        v
+---------------------------+
| AgentCore Runtime         |
| isolated managed compute  |
+-------------+-------------+
              |
              v
      BedrockAgentCoreApp
              |
              v
       @app.entrypoint
        handler(request)
              |
              v
        plain Python
              |
              v
        JSON response
```

### Responsibility map

| Layer | Responsibility |
|---|---|
| AgentCore CLI/client | sends the request |
| AgentCore Runtime | runs and isolates the application |
| `BedrockAgentCoreApp` | exposes the application entrypoint |
| your handler | decides the response |
| foundation model | **not used today** |

---

## Important terms

### Runtime

The managed environment in which the agent application executes.

### Entrypoint

The function AgentCore calls when the Runtime receives an invocation.

### Payload

The application data sent to the entrypoint, such as:

```json
{"prompt": "hello"}
```

---

## Read the code

Open [main.py](main.py).

There are only three ideas.

### 1. Create the Runtime application wrapper

```python
app = BedrockAgentCoreApp()
```

### 2. Mark the invocation handler

```python
@app.entrypoint
def handler(request):
```

### 3. Return deterministic Python output

```python
return {
    "message": f"Runtime received: {prompt}",
    "handled_by": "plain-python",
}
```

The `handled_by` field is intentionally included so the learner can see that no LLM generated the answer.

---

## Predict before running

Write down your prediction for each case.

### Prediction A

Input:

```text
hello
```

Will the wording change creatively between calls?

**Expected prediction:** No. It is deterministic Python.

### Prediction B

Input:

```text
health
```

Who creates the response?

**Expected prediction:** the Python handler.

### Prediction C

Input with no valid prompt.

What should happen?

**Expected prediction:** input validation returns a controlled error response.

---

## Run it

### 1. Install the current AgentCore CLI

```bash
npm install -g @aws/agentcore
agentcore --help
```

### 2. Create a current project scaffold

```bash
agentcore create --name Day01Runtime --framework Strands --model-provider Bedrock --memory none --build CodeZip --protocol HTTP
cd Day01Runtime
```

The generated entrypoint is:

```text
app/Day01Runtime/main.py
```

Replace that generated file with this day’s [main.py](main.py).

Make sure the generated Python project includes `bedrock-agentcore`.

### 3. Local development

```bash
agentcore dev
```

In another terminal:

```bash
agentcore dev "hello"
agentcore dev "health"
```

### 4. Deploy

```bash
agentcore deploy
```

### 5. Invoke the deployed Runtime

```bash
agentcore invoke "hello"
agentcore invoke "health"
```

---

## Expected evidence

You should see structurally similar output to:

```json
{
  "ok": true,
  "message": "Runtime received: hello",
  "handled_by": "plain-python"
}
```

and:

```json
{
  "ok": true,
  "message": "Runtime application is healthy.",
  "handled_by": "plain-python"
}
```

The exact wrapper printed by the CLI may differ. The important evidence is the application response.

---

## Break it on purpose

Change:

```python
prompt = request.get("prompt")
```

to look for a nonexistent field:

```python
prompt = request.get("question")
```

Invoke again.

### What should you learn?

The Runtime can be healthy while **your application contract is wrong**.

That distinction matters later when debugging models, tools, and Memory.

Restore the code afterward.

---

## Learner assignment

Add a deterministic command:

```text
version
```

that returns:

```json
{
  "ok": true,
  "message": "day-01-v1"
}
```

Then:

1. run locally,
2. deploy,
3. invoke the deployed Runtime,
4. capture both outputs.

---

## Explain-back test

Without looking at this README, answer:

1. What does AgentCore Runtime do?
2. What does `@app.entrypoint` identify?
3. Is a foundation model involved today?
4. If the response is wrong, which two broad layers would you check first?
5. What is the difference between the Runtime and your handler?

If those answers are unclear, repeat Day 1 before moving on.

---

## Production gap

This example intentionally does **not** include:

- authentication,
- model inference,
- Memory,
- retries,
- observability configuration,
- tools,
- business logic.

That is not a weakness. It is what makes the Runtime boundary visible.

---

## Next day

Day 2 adds exactly one new component:

```text
Runtime -> Amazon Bedrock model
```

That will let you see the difference between **the platform hosting your application** and **the service performing model inference**.

---

[Course index](../README.md) · [Teaching standard](../TEACHING_STANDARD.md)
