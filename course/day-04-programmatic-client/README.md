# Day 04 — Build the Runtime Client Yourself

## Today’s question

> In a real application, who creates and reuses the `runtimeSessionId`?

---

## Why should I care?

The AgentCore CLI is excellent for learning and operations, but your production application will usually invoke Runtime from:

- a backend API,
- web application,
- mobile application,
- service,
- workflow,
- another agent.

That caller must understand the difference between **Runtime metadata** and the **application payload**.

Today you build that caller yourself.

---

## One-sentence mental model

> **Your client/backend sends both the application payload and the Runtime session identifier; the payload goes to your agent code, while `runtimeSessionId` controls which Runtime session handles the invocation.**

---

## Build on yesterday

### Day 3

The CLI supplied the session ID:

```text
agentcore invoke --session-id ...
```

### Day 4

Your code does it:

```text
Python client
   |
   | runtimeSessionId = session-A
   | payload = {"prompt": "hello"}
   v
InvokeAgentRuntime
   |
   v
AgentCore Runtime
```

---

## Architecture / request flow

```text
User types:
"first request"
       |
       v
client.py
       |
       +--> builds JSON payload
       |      {"prompt": "first request"}
       |
       +--> chooses runtimeSessionId
       |      day04-...
       |
       v
boto3 bedrock-agentcore client
       |
       | invoke_agent_runtime(...)
       v
AgentCore Runtime
       |
       v
Day 3 application
       |
       v
JSON response
       |
       v
client.py prints result
```

### Two different channels of information

```text
Runtime metadata:
runtimeSessionId

Application payload:
{"prompt": "..."}
```

Do not put `runtimeSessionId` into your JSON payload just because the Runtime API also has a session ID.

They serve different purposes.

---

## Important terms

### `InvokeAgentRuntime`

The AgentCore data-plane operation used to invoke a deployed Runtime programmatically.

### Runtime ARN

Identifies the deployed AgentCore Runtime.

### Session mapping

The relationship your application maintains between a user/conversation and the corresponding Runtime session ID.

Example:

```text
user-42
  -> conversation-orders
      -> runtimeSessionId abc...
```

---

## Read the code

Open [client.py](client.py).

### 1. Build the application payload

```python
payload = json.dumps({"prompt": prompt}).encode("utf-8")
```

### 2. Send the session ID separately

```python
response = client.invoke_agent_runtime(
    agentRuntimeArn=AGENT_RUNTIME_ARN,
    runtimeSessionId=session_id,
    payload=payload,
)
```

This is the key line for Day 4.

### 3. Reuse the same session

The chat loop keeps:

```python
session_id
```

unchanged until you type:

```text
/new
```

That lets you observe the Day 3 state model directly.

---

## Predict before running

Use the Day 3 Runtime as the target.

### Prediction A

Start the client and send:

```text
hello
again
```

Expected:

```text
turn 1
turn 2
```

### Prediction B

Type:

```text
/new
```

Then send:

```text
hello
```

Expected:

```text
turn 1
```

### Prediction C

Change only the prompt, but keep the same session ID.

Expected:

The same Runtime session remains associated with the conversation.

---

## Run it

First deploy the Day 3 agent.

Get its Runtime information:

```bash
agentcore status
```

Set:

```bash
export AGENT_RUNTIME_ARN="<YOUR_RUNTIME_ARN>"
export AWS_REGION="<YOUR_REGION>"
```

Install boto3 if needed:

```bash
pip install boto3
```

Run:

```bash
python client.py
```

Example interaction:

```text
AgentCore Day 4 client
Session: day04-...

You: hello
...
You: again
...
You: /id
Current session: day04-...
You: /new
New session: day04-...
You: hello
...
```

---

## Expected evidence

The important evidence is:

```text
same session ID:
turn 1 -> turn 2 -> turn 3

/new:
new session ID

new session:
turn 1
```

You should also see the session ID returned alongside the agent response.

---

## Break it on purpose

Modify:

```python
runtimeSessionId=session_id
```

so a new session ID is generated inside `invoke_agent()` for every request.

Then chat twice.

### What should happen?

Every request should behave like a new conversation/session.

### What should you learn?

A client bug can destroy session continuity even when the Runtime and agent code are perfectly healthy.

---

## Learner assignment

Add simple user switching.

For example:

```text
/switch alice
/switch bob
```

Maintain:

```python
user_sessions = {
    "alice": "<session-id-A>",
    "bob": "<session-id-B>",
}
```

Prove:

- Alice's Runtime state continues when you switch back to Alice.
- Bob gets a separate Runtime session.
- Neither user needs the session ID inside the JSON payload.

---

## Explain-back test

1. Who creates the Runtime session ID?
2. What is the difference between `runtimeSessionId` and the JSON payload?
3. What does the Runtime ARN identify?
4. Why should a backend maintain user-to-session mappings?
5. What bug occurs if you create a new session ID for every message?

---

## Production gap

A real client/backend also needs:

- user authentication,
- authorization to sessions,
- secure session lookup/storage,
- retry/backoff,
- timeout handling,
- streaming response handling,
- observability,
- protection against users supplying another user's session identifier.

AgentCore does not replace your application's user/session ownership model.

---

## Next day

Runtime session state is useful but ephemeral.

Day 5 introduces the separate service used when information must survive beyond the current Runtime compute lifecycle:

```text
AgentCore Memory
```

---

[Course index](../README.md) · [Teaching standard](../TEACHING_STANDARD.md)
