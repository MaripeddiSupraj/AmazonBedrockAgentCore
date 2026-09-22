# Part 08 — Deploy a Short-Term Memory Agent

**AgentCore capability:** Memory

This is the first lab in the series that uses **AgentCore Memory** instead of pretending that in-process Python state is durable memory.

The most important lesson is the identity model:

```text
memory_id
  |
  +-- actor_id = who/entity this memory belongs to
        |
        +-- session_id = one logical conversation
              |
              +-- USER message
              +-- ASSISTANT message
              +-- USER message
              +-- ASSISTANT message
```

The USER/ASSISTANT value is a **message role**. It is not the actor ID.

---

## 1. What you will learn

By the end of the lab you should be able to explain:

- what an AgentCore Memory resource is,
- what short-term memory stores,
- the difference between `actor_id`, `session_id`, and message `role`,
- why the same actor can have multiple sessions,
- why Runtime session state and AgentCore Memory are different concepts,
- how conversation events are written and reconstructed.

---

## 2. Why Part 05 was not enough

Part 05 uses state inside the running application.

Conceptually:

```text
Python process
   |
   +--> local dict/list
```

If that execution environment disappears, the application should not treat that local state as durable memory.

Part 08 introduces a separate service:

```text
Agent Runtime
     |
     +--------------------+
     |                    |
     v                    v
 Bedrock model       AgentCore Memory
                          |
                          +--> actor
                                |
                                +--> session
                                      |
                                      +--> events
```

That separation is fundamental to production agent design.

---

## 3. Four identifiers/concepts people commonly mix up

### `MEMORY_ID`

Identifies the AgentCore Memory resource.

Think:

> Which memory database/resource am I using?

### `actor_id`

Identifies the entity whose activity/memory is being stored.

Typical examples:

```text
user-123
customer-456
support-agent/user-123
```

Think:

> Whose memory is this?

### `session_id`

Groups related events into one logical conversation/workflow.

Examples:

```text
order-support-001
travel-planning-2026-09
incident-INC123
```

Think:

> Which conversation does this event belong to?

### message role

Inside an event, the conversational role describes **who said the message in the conversation**:

```text
USER
ASSISTANT
TOOL
OTHER
```

Do not model this as:

```text
actor_id = USER
actor_id = ASSISTANT
```

because then you split one user's conversation across different actors and lose the clean actor/session boundary.

---

## 4. Request flow

For a new message:

```text
Client
  |
  | prompt
  | actor_id=user-123
  | memory_session_id=chat-001
  v
AgentCore Runtime
  |
  v
agent/mystmagent.py
  |
  | 1. create_event(USER)
  v
AgentCore Memory
  |
  | 2. list_events(actor=user-123, session=chat-001)
  v
reconstructed conversation
  |
  | 3. send history to Bedrock model
  v
LLM response
  |
  | 4. create_event(ASSISTANT)
  v
AgentCore Memory
  |
  v
response to caller
```

Notice that both USER and ASSISTANT messages are stored under the **same actor and session**.

---

## 5. Runtime session vs Memory session

These are related ideas but not the same resource.

### Runtime session

Controls the isolated Runtime execution context.

### Memory session

Groups memory events logically inside AgentCore Memory.

For a simple application you may choose to map them together, but do not assume AgentCore automatically makes them the same identifier.

This lab passes an explicit application payload field called:

```text
memory_session_id
```

so the distinction is visible while learning.

---

## 6. Configuration

The updated example reads configuration from environment variables instead of hardcoding a real Memory resource:

```bash
export AWS_REGION=us-east-1
export MEMORY_ID="<YOUR_MEMORY_ID>"
export MODEL_ID="<A_CLAUDE_MODEL_AVAILABLE_IN_YOUR_ACCOUNT>"
```

Model IDs and availability change over time and by Region/account. Use one that supports the Anthropic Messages request shape used in this lab.

---

## 7. Example payloads

### Same actor, same session

First request:

```json
{
  "prompt": "My favorite database is PostgreSQL.",
  "actor_id": "user-123",
  "memory_session_id": "chat-001"
}
```

Second request:

```json
{
  "prompt": "What database did I say I like?",
  "actor_id": "user-123",
  "memory_session_id": "chat-001"
}
```

The second request can reconstruct the earlier conversation from short-term Memory.

### Same actor, different session

```json
{
  "prompt": "What database did I say I like?",
  "actor_id": "user-123",
  "memory_session_id": "chat-002"
}
```

This is a different logical session. Do not expect `chat-001` short-term history to appear automatically in `chat-002`.

That cross-session learning problem is where **long-term memory strategies** become important in later labs.

### Different actor

```json
{
  "prompt": "What database did I say I like?",
  "actor_id": "user-999",
  "memory_session_id": "chat-001"
}
```

This should not inherit `user-123`'s conversation.

---

## 8. Reset only one actor/session

Send:

```json
{
  "prompt": "reset",
  "actor_id": "user-123",
  "memory_session_id": "chat-001"
}
```

The example deletes events for that actor/session pair rather than using global USER/ASSISTANT actor buckets.

---

## 9. Code walkthrough

Open:

```text
agent/mystmagent.py
```

Follow these functions in order:

### `store_message(...)`

Calls `MemoryClient.create_event()`.

Look for:

```python
actor_id=actor_id
session_id=session_id
messages=[(text, role)]
```

That line is the core data model.

### `load_conversation(...)`

Calls `list_events()` for the same actor/session and converts stored conversational payloads back into model messages.

### `invoke(...)`

The entrypoint:

1. validates configuration,
2. reads prompt/actor/session,
3. stores USER event,
4. loads history,
5. calls Bedrock,
6. stores ASSISTANT event,
7. returns the response.

---

## 10. Prerequisites

- Part 03–05 concepts understood
- AgentCore Memory resource
- required Memory data-plane permissions
- Bedrock model access
- Runtime execution role allowed to call both Memory and Bedrock Runtime

Use the policies in this repo only as educational starting points; scope permissions appropriately for your environment.

---

## 11. Learner assignment

Create this test matrix:

| Test | actor_id | memory_session_id | Expected |
|---|---|---|---|
| A1 | user-123 | chat-001 | store a fact |
| A2 | user-123 | chat-001 | recall the fact |
| B1 | user-123 | chat-002 | should not receive chat-001 history as STM |
| C1 | user-999 | chat-001 | should not receive user-123 history |

Then inspect the events in AgentCore Memory.

---

## 12. Success criteria

You understand Part 08 when you can explain this sentence precisely:

> AgentCore short-term Memory stores immutable conversation events under a Memory resource, scoped by an actor and session, while USER/ASSISTANT describe the role of each conversational message.

And you can draw:

```text
Memory
  -> actor user-123
       -> session chat-001
            -> USER
            -> ASSISTANT
       -> session chat-002

  -> actor user-999
       -> session chat-001
```

---

## 13. What comes next

Part 08 answers:

> How do I persist conversation events for a session?

Parts 09/11/13 answer a different question:

> How do I extract and retrieve useful information that should survive beyond one short-term conversation?

That distinction is **short-term events vs long-term memory records/strategies**.

---

[← Back to the lab index](../README.md) · [Learning guide](../LEARNING_GUIDE.md)
