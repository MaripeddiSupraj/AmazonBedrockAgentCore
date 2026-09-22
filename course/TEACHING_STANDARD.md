# Teaching Standard for AgentCore Course Labs

This file defines the format that **OpenCode, Claude Code, contributors, and future maintainers should follow** when extending the course.

The standard exists because runnable code is not automatically good teaching material.

---

## 1. Primary goal

Each day should teach **one major mental model**.

Good:

```text
Day 3 = Runtime sessions and ephemeral state
```

Bad:

```text
Day 3 = Runtime + Memory + Gateway + OAuth + Browser + observability
```

A learner should know exactly what new idea was added compared with the previous day.

---

## 2. Use a concept budget

Every day gets:

- **1 major new concept**
- at most **2–3 supporting terms**
- one primary architecture flow
- one core code path

If more concepts are required, split the lesson.

---

## 3. Required README structure

Every course day MUST contain these sections in this order.

### 1. Today’s question

One plain-English question.

Example:

> What does `runtimeSessionId` actually do?

### 2. Why should I care?

Explain the real problem before introducing AWS terminology.

### 3. One-sentence mental model

Example:

> A Runtime session is an isolated execution environment identified by a session ID; its in-memory state is useful during the session but is not durable Memory.

### 4. Build on yesterday

Show only what changed.

Example:

```text
Yesterday:
Client -> Runtime -> Model

Today:
Client --runtimeSessionId--> dedicated Runtime session -> application state
```

### 5. Architecture / request flow

Use a small ASCII diagram. Do not hide the important boundary.

### 6. Important terms

Maximum 3–5 terms. Define them in one or two sentences each.

### 7. Read the code

Walk through the core file in execution order.

Do not explain every import.

### 8. Predict before running

Give 2–4 predictions.

Example:

- same session ID -> counter increases,
- different session ID -> separate state,
- stopped microVM -> in-memory state disappears.

### 9. Run it

Commands must be copyable.

Label historical commands if they are historical.

### 10. Expected evidence

Show what the learner should observe.

Avoid exact LLM wording when output is probabilistic. Test structural behavior instead.

### 11. Break it on purpose

Every day needs one failure experiment.

Examples:

- invalid model ID,
- new session ID,
- missing Memory ID,
- denied IAM permission,
- wrong actor/session.

### 12. Learner assignment

The learner must modify the code.

Copying the provided sample is not an assignment.

### 13. Explain-back test

3–5 questions the learner should answer without reading the README.

### 14. Production gap

State clearly what the educational example does **not** solve.

### 15. Cleanup / cost hygiene

Every AWS-backed lesson must say:

- which resources were created,
- whether the next day reuses them,
- when to keep them,
- how to remove them safely.

For current CLI-managed course projects, prefer the explicit teardown flow:

```bash
agentcore remove all
agentcore deploy
```

Do not teach cloud labs that silently leave resources behind.

### 16. Next day

Explain why the next concept is needed.

---

## 4. Code standard

Core teaching code should normally stay under roughly **80–120 lines**.

Priorities:

1. correctness,
2. clarity,
3. visible execution flow,
4. current APIs,
5. safe configuration,
6. only then abstractions.

Avoid:

- unnecessary classes,
- helper layers that hide the API being taught,
- hardcoded account IDs, ARNs, Memory IDs, secrets, or API keys,
- unexplained magic constants,
- old model-specific request schemas when a current common API is clearer,
- broad exception handling that hides the actual failure.

Prefer:

```python
MODEL_ID = os.environ["MODEL_ID"]
```

over:

```python
MODEL_ID = "some-old-model-id"
```

---

## 5. Example standard

Examples should use **observable behavior**, not vague chat.

Weak example:

> Ask the model anything and see that it works.

Strong example:

> Ask it to return exactly three reasons containers are useful. Confirm the response came from a model, then deliberately set an invalid model ID and observe where the failure occurs.

For sessions:

Weak:

> Chat twice.

Strong:

```text
session-A -> call 1 -> turn 1
session-A -> call 2 -> turn 2
session-B -> call 1 -> turn 1
```

For Memory:

Weak:

> The agent remembers.

Strong:

```text
actor=user-123, session=chat-001 -> store event
same actor/session -> event is listed
new runtime compute -> event still exists in AgentCore Memory
different actor -> event is not part of that actor's history
```

---

## 6. Use the current product model

When a service or CLI changes, update the main course.

Historical material may remain under the older `part-*` labs, but the course should teach current concepts.

As of this course redesign:

```text
Current AgentCore CLI:
create -> dev -> deploy -> invoke
```

Do not teach legacy `agentcore launch` as the default workflow.

---

## 7. Separate platform layers explicitly

Every lesson should identify which layer performs each responsibility.

Example:

```text
AgentCore Runtime
= hosts/isolate/runs the agent application

Amazon Bedrock Runtime
= performs model inference

AgentCore Memory
= persists agent memory events/records

Your client
= owns the mapping between users and runtime session IDs
```

Never let learners conclude these are one service.

---

## 8. Distinguish ephemeral and durable state

This is a mandatory teaching theme.

Always distinguish:

```text
Runtime session state
- process memory
- local ephemeral filesystem
- tied to session compute lifecycle

AgentCore Memory
- separate service
- short-term events / long-term records
- persists independently of the current microVM lifecycle
```

Do not describe Python globals as durable Memory.

---

## 9. Evidence standard

Every lab must define evidence.

Acceptable evidence:

- response JSON,
- counter difference across sessions,
- Runtime logs,
- model request/response behavior,
- Memory events,
- Gateway tool listing,
- policy allow/deny result,
- trace/span,
- evaluator result.

"Command exited successfully" alone is insufficient.

---

## 10. Production notes must be factual

Do not call educational code production-ready.

Identify missing concerns such as:

- least-privilege IAM,
- authentication,
- retries/backoff,
- timeouts,
- streaming,
- quotas,
- cost controls,
- model fallbacks,
- validation,
- observability,
- PII handling,
- cleanup,
- testing.

Only list concerns relevant to that day's scope.

---

## 11. Keep the learner active

Each day should include all three:

### Predict

What will happen?

### Prove

What evidence shows it happened?

### Modify

Can the learner change behavior?

This is the core teaching loop:

```text
Understand -> Predict -> Run -> Observe -> Break -> Modify -> Explain
```

---

## 12. OpenCode continuation rule

When asked to create Day 6 onward:

1. read `course/README.md`,
2. read this file,
3. inspect Days 1–5,
4. inspect current AWS documentation for the capability,
5. use the same section order,
6. add only one major new mental model,
7. keep the core code minimal,
8. include a break-it experiment,
9. include an assignment and explain-back test,
10. include cleanup/cost guidance,
11. link the day back into `course/README.md`.

Do not copy an older `part-*` README verbatim. Use old labs only as implementation references.
