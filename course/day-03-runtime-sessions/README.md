# Day 03 — Runtime Sessions and Ephemeral State

## Today’s question

> What does `runtimeSessionId` actually give me, and why is that still not durable Memory?

---

## Why should I care?

Agents are not ordinary stateless request/response functions.

A long-running task may need:

- intermediate variables,
- downloaded files,
- conversation state,
- tool outputs,
- working notes.

AgentCore Runtime can keep that state available **inside one isolated Runtime session**.

But this creates an important trap:

> "The agent remembered something, so I have durable Memory."

Not necessarily.

Today you learn the difference.

---

## One-sentence mental model

> **A Runtime session gives one conversation/workflow an isolated execution environment whose in-process state can survive multiple invocations during that compute lifecycle, but that state is ephemeral and should not be treated as durable AgentCore Memory.**

---

## Build on yesterday

### Day 2

```text
Client -> Runtime -> model -> response
```

### Day 3

For teaching session behavior, we temporarily use deterministic Python again:

```text
Client
  |
  | runtimeSessionId = A
  v
+--------------------------+
| dedicated Runtime session|
| process memory           |
| SESSION_STATE            |
+--------------------------+
```

A second session gets a separate environment:

```text
session A -> microVM/environment A -> state A
session B -> microVM/environment B -> state B
```

---

## Architecture / request flow

```text
Invocation 1
runtimeSessionId = session-A
        |
        v
+-----------------------------+
| Runtime environment A       |
| SESSION_STATE["turn"] = 1   |
+-----------------------------+

Invocation 2
runtimeSessionId = session-A
        |
        v
+-----------------------------+
| SAME session environment A  |
| SESSION_STATE["turn"] = 2   |
+-----------------------------+

Invocation 3
runtimeSessionId = session-B
        |
        v
+-----------------------------+
| separate environment B      |
| SESSION_STATE["turn"] = 1   |
+-----------------------------+
```

The session ID is **Runtime routing/session metadata**.

It is not something your client must duplicate inside:

```json
{"prompt": "..."}
```

unless your application has a separate business reason to do so.

---

## Important terms

### `runtimeSessionId`

Identifies a Runtime session.

Related invocations should reuse the same ID.

### Session isolation

Different Runtime sessions receive isolated execution environments, preventing state from one session leaking into another.

### Ephemeral state

State that exists only for the current compute lifecycle, such as Python globals or ordinary local files.

---

## Read the code

Open [main.py](main.py).

The entire lesson is visible in:

```python
SESSION_STATE = {
    "turn": 0,
    "prompts": [],
}
```

Each invocation increments:

```python
SESSION_STATE["turn"] += 1
```

The response shows:

- current turn,
- prompts seen in the current compute,
- the state type.

There is deliberately no dictionary keyed by `runtimeSessionId`.

Why?

Because the Runtime session is already the isolation boundary.

The session ID is used by the Runtime/client layer to route related invocations to the session environment.

---

## Predict before running

Use two long session IDs:

```text
day03-session-A-123456789012345678901234567890
day03-session-B-123456789012345678901234567890
```

### Prediction A

Call session A twice.

Expected turns:

```text
1
2
```

### Prediction B

Call session B once.

Expected turn:

```text
1
```

### Prediction C

Stop/lose the underlying ephemeral compute and later resume the logical session without persistent storage.

Should you trust the Python global to survive?

**Expected:** No.

---

## Run it

Create and deploy the project as in earlier days:

```bash
agentcore create --name Day03Session --defaults
cd Day03Session
```

Replace:

```text
app/Day03Session/main.py
```

with [main.py](main.py).

Then:

```bash
agentcore deploy
```

### Same Runtime session

```bash
agentcore invoke   --session-id day03-session-A-123456789012345678901234567890   "first request"

agentcore invoke   --session-id day03-session-A-123456789012345678901234567890   "second request"
```

### Different Runtime session

```bash
agentcore invoke   --session-id day03-session-B-123456789012345678901234567890   "first request in B"
```

---

## Expected evidence

Session A should conceptually show:

```text
first request  -> turn 1
second request -> turn 2
```

Session B should begin independently:

```text
first request in B -> turn 1
```

The important evidence is **isolation and continuity within the active session**, not exact JSON formatting from the CLI.

---

## Break it on purpose

Invoke with a brand-new session ID every time.

Example:

```bash
agentcore invoke --session-id day03-new-111111111111111111111111111111 "hello"
agentcore invoke --session-id day03-new-222222222222222222222222222222 "hello again"
```

### What should you learn?

The session ID is part of your application’s conversation/session lifecycle design.

If your client generates a new one for every request, you lose session continuity.

---

## A subtle but important point

AgentCore does **not** decide which user should own which session ID.

Your client/backend should maintain:

```text
user -> conversation -> runtimeSessionId
```

Do not expose unrestricted session IDs and assume the platform will map them safely to your end users for you.

---

## Learner assignment

Add another piece of process-local state:

```python
"last_prompt": None
```

Return both:

```text
current_prompt
previous_prompt
```

Then prove:

- session A sees its own previous prompt,
- session B does not see session A's previous prompt.

---

## Explain-back test

1. What does `runtimeSessionId` identify?
2. Is it part of the business JSON payload or Runtime invocation metadata?
3. Why can a Python global appear to "remember" during a session?
4. Why is that not durable Memory?
5. What happens when you use a different session ID?

---

## Production gap

This example does not persist state outside the Runtime session.

That means you should not use it for durable:

- conversation history,
- learned user preferences,
- important business facts,
- audit records.

Runtime session storage options can preserve certain filesystem data across compute stop/resume, but structured agent memory is a separate problem.

---

## Next day

Day 4 teaches the component that actually owns the session ID in a real application:

```text
your client/backend
      |
      v
InvokeAgentRuntime
      |
      v
runtimeSessionId
```

You will stop relying only on the CLI and write the caller yourself.

---

[Course index](../README.md) · [Teaching standard](../TEACHING_STANDARD.md)
