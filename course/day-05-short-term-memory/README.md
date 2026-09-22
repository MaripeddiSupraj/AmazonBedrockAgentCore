# Day 05 — AgentCore Short-Term Memory

## Today’s question

> If Runtime session state disappears with the compute lifecycle, where should an agent store conversation events that must survive beyond that microVM?

---

## Why should I care?

Day 3 proved that Runtime session state can be useful.

But process memory is not durable.

If you need conversation events to outlive the current Runtime compute, you need a separate persistence layer.

Today we add exactly one new component:

```text
AgentCore Memory
```

---

## One-sentence mental model

> **AgentCore Memory is a separate managed service that stores agent events outside the Runtime microVM, organized by Memory resource, actor, and logical memory session.**

---

## Build on yesterday

### Day 3 / Day 4

```text
client
  |
  | runtimeSessionId
  v
Runtime session
  |
  +--> Python globals
       ephemeral
```

### Day 5

```text
client
  |
  v
Runtime session
  |
  | create_event(...)
  v
AgentCore Memory
  |
  +--> actor
        |
        +--> memory session
              |
              +--> immutable events
```

Now the important state is outside the Runtime compute.

---

## Architecture / request flow

### Store an event

```text
Prompt:
"I prefer PostgreSQL"
        |
        v
AgentCore Runtime
        |
        v
main.py
        |
        | MemoryClient.create_event()
        v
AgentCore Memory
        |
        +--> MEMORY_ID
              |
              +--> actor = learner-001
                    |
                    +--> session = day05-memory-session
                          |
                          +--> USER event
```

### Read the history

```text
"/history"
     |
     v
Runtime
     |
     | MemoryClient.list_events()
     v
AgentCore Memory
     |
     v
stored events
     |
     v
response
```

---

## The four IDs/labels you must not mix up

### 1. Runtime session ID

```text
runtimeSessionId
```

Used by AgentCore Runtime to identify the isolated execution session.

### 2. Memory resource ID

```text
MEMORY_ID
```

Identifies the AgentCore Memory resource.

### 3. Actor ID

```text
learner-001
```

Identifies the entity the memory belongs to.

Think:

> Whose memory is this?

### 4. Memory session ID

```text
day05-memory-session
```

Groups related Memory events.

Think:

> Which logical conversation do these events belong to?

And inside each conversational event:

```text
USER / ASSISTANT / TOOL / OTHER
```

is the **message role**, not the actor ID.

---

## Why the example does not use an LLM

This is deliberate.

A model would add another moving part and distract from the Memory data model.

Today the learning target is:

```text
write event
read event
change Runtime session
read the same durable event
```

Later labs can combine Memory with a model.

---

## Read the code

Open:

- [setup_memory.py](setup_memory.py)
- [main.py](main.py)

### 1. Create the Memory resource

```python
memory = client.create_memory_and_wait(
    name="CourseDay05Memory",
    strategies=[],
)
```

No long-term strategy is added today.

We are learning short-term Memory events only.

### 2. Store one event

```python
event = memory.create_event(
    memory_id=MEMORY_ID,
    actor_id=actor_id,
    session_id=memory_session_id,
    messages=[(prompt, "USER")],
    extraction_mode="SKIP",
)
```

The important structure is:

```text
Memory
  -> actor
       -> session
            -> event
```

### 3. Read the events

```python
events = memory.list_events(
    memory_id=MEMORY_ID,
    actor_id=actor_id,
    session_id=memory_session_id,
)
```

The code converts the conversational payloads into a simple history response.

---

## Predict before running

### Prediction A

Runtime session A stores:

```text
I prefer PostgreSQL
```

Then the same Runtime session calls:

```text
/history
```

Expected:

The event appears.

### Prediction B

Use a completely different Runtime session ID, but keep the same Memory actor/session.

Call:

```text
/history
```

Expected:

The event still appears because it lives in AgentCore Memory, not in the previous microVM.

### Prediction C

Change the actor from:

```text
learner-001
```

to another actor in a programmatic payload.

Expected:

That actor has a separate Memory scope.

---

## Run it

### 1. Create a Memory resource

From this folder:

```bash
export AWS_REGION="<YOUR_REGION>"
pip install bedrock-agentcore boto3
python setup_memory.py
```

The script prints:

```text
MEMORY_ID=...
```

Export it:

```bash
export MEMORY_ID="<THE_PRINTED_MEMORY_ID>"
```

You can also create/manage Memory through the current AgentCore CLI using `agentcore add memory`. This setup script is intentionally explicit so the learner sees the Memory resource separately from Runtime.

### 2. Create the Runtime project

```bash
agentcore create --name Day05Memory --defaults
cd Day05Memory
```

Replace:

```text
app/Day05Memory/main.py
```

with this day’s [main.py](main.py).

Make sure the Runtime execution role can perform the Memory operations used in this lesson, including:

```text
bedrock-agentcore:CreateEvent
bedrock-agentcore:ListEvents
```

against the intended Memory resource.

Deploy:

```bash
agentcore deploy
```

---

## The key experiment

Use two different Runtime session IDs.

### Runtime session A stores the event

```bash
agentcore invoke   --session-id day05-runtime-A-123456789012345678901234567890   "I prefer PostgreSQL"
```

### Runtime session B reads it

```bash
agentcore invoke   --session-id day05-runtime-B-123456789012345678901234567890   "/history"
```

The Runtime session changed.

The default Memory scope did not:

```text
actor_id = learner-001
memory_session_id = day05-memory-session
```

---

## Expected evidence

The `/history` response from Runtime session B should include the event stored while using Runtime session A.

That proves:

```text
Runtime microVM A
      X
      | state does not need to survive here
      |
AgentCore Memory
      |
      v
Runtime microVM B can read the event
```

This is the most important proof in the first five days.

---

## Break it on purpose

Temporarily set an incorrect:

```text
MEMORY_ID
```

and invoke the agent.

### What should you learn?

The Runtime can be healthy while the separate Memory service call fails.

This gives you another debugging boundary:

```text
Runtime healthy?
Memory resource correct?
IAM allowed?
actor/session correct?
```

Restore the correct Memory ID afterward.

---

## Learner assignment

Use the Day 4 programmatic client idea to send custom payload fields:

```json
{
  "prompt": "My preferred database is PostgreSQL",
  "actor_id": "alice",
  "memory_session_id": "preferences-001"
}
```

Then create:

```text
alice / preferences-001
bob   / preferences-001
```

Prove:

- Alice's history contains Alice's event.
- Bob's history does not inherit Alice's event.
- both can be called from new Runtime sessions.

---

## Explain-back test

1. What is the difference between a Runtime session and a Memory session?
2. What does `actor_id` represent?
3. Is USER an actor ID or a conversational role?
4. Why can a new Runtime microVM still read an old Memory event?
5. What does `extraction_mode="SKIP"` communicate in this lesson?
6. Why did we deliberately avoid adding an LLM today?

---

## Production gap

This lesson stores and lists short-term events.

It does not yet solve:

- long-term semantic retrieval,
- preference extraction,
- summarization,
- episodic memory,
- retention design,
- PII/privacy policy,
- deletion workflows,
- large-session pagination strategy,
- model context-window management.

Those are later lessons.

---

## What you should understand after Day 5

You should now be able to draw this without help:

```text
                    +----------------------+
Client ------------>| AgentCore Runtime    |
 runtimeSessionId   | isolated execution   |
                    +----------+-----------+
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
          Bedrock model               AgentCore Memory
          inference                    actor/session/events
          (Day 2)                      (Day 5)
```

And explain:

```text
Runtime session state = useful, isolated, ephemeral
AgentCore Memory      = separate durable agent-memory service
```

If that distinction is clear, the foundation is strong enough to move into long-term Memory, Gateway, Identity, tools, policy, observability, and evaluations.

---

[Course index](../README.md) · [Teaching standard](../TEACHING_STANDARD.md)
