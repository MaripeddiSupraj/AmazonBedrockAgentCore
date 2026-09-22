# Amazon Bedrock AgentCore — Learning Guide

This guide turns the repository from a collection of runnable labs into a structured learning path.

The goal is not only to make the examples run. By the end, a learner should be able to explain:

1. **What problem each AgentCore service solves**
2. **Why that service exists**
3. **What happens behind the scenes**
4. **Which code/configuration is responsible for each step**
5. **How to prove the behavior works**
6. **What would need to change before production**

> **Important (September 2026):** The Python `bedrock-agentcore-starter-toolkit` used by many early labs is now a legacy/unsupported CLI for new projects. The current recommended CLI is `@aws/agentcore`. The older labs are still useful for learning the concepts and SDK patterns, but always compare deployment commands with the current AWS documentation before using them in a new project.

---

## 1. The mental model: what AgentCore gives you

Think of an AI agent as an application that can reason, remember, use tools, act on behalf of users, and run for longer than one HTTP request.

A normal application platform gives you compute, networking, logs, and security primitives. AgentCore adds agent-specific primitives around those needs.

| Capability | Simple mental model | Problem it solves |
|---|---|---|
| **Runtime** | Where the agent runs | Secure, managed execution and session isolation |
| **Memory** | What the agent can remember | Durable conversational history and learned information |
| **Gateway** | Controlled front door to tools | Expose APIs/Lambda/tools to agents through MCP |
| **Identity** | Who the agent/user is and what credentials it may use | Inbound and outbound authentication/authorization |
| **Code Interpreter** | Managed code execution room | Safe calculations, analysis, files, and generated code |
| **Browser** | Managed browser session | Web navigation and browser automation |
| **Observability** | Flight recorder | Traces, logs, metrics, and debugging across agent steps |
| **Policy** | Guardrail at the action boundary | Decide whether a tool/action should be allowed |
| **Evaluations** | Quality test system | Measure whether agent behavior meets expectations |
| **Registry** | Service catalog for agents/tools | Discover approved agents, MCP servers, and resources |
| **Payments** | Commercial action/payment plumbing | Payment-aware agent workflows |

---

## 2. Two flows every learner must understand

### A. Deployment flow

For new projects, think in terms of the current AgentCore CLI:

```text
Agent source code
      |
      v
agentcore create/configuration
      |
      v
agentcore dev                 <- local development
      |
      v
agentcore deploy
      |
      +--> package/build application
      +--> create/update required AWS resources
      +--> create a Runtime version/endpoint
      +--> attach execution permissions/configuration
      |
      v
Runtime endpoint becomes ready
```

Many early labs use the older Starter Toolkit flow:

```text
agentcore configure
      |
      v
agentcore launch
      |
      v
AgentCore Runtime
```

The important concept is the same: **local agent code is converted into a managed Runtime deployment**. Do not memorize `launch` as the current command for new projects.

### B. Invocation flow

```text
Client/application
      |
      | prompt + runtime/session identity
      v
AgentCore Runtime
      |
      +--> resolve/create isolated session environment
      |
      v
Agent application
      |
      +--> call model
      +--> read/write memory (optional)
      +--> call Gateway/tools (optional)
      +--> use Browser/Code Interpreter (optional)
      |
      v
response
      |
      v
Client/application
```

The Runtime session and AgentCore Memory are **not the same thing**:

- Runtime session state is execution context.
- AgentCore Memory is a separate durable memory service.
- If a microVM/session disappears, do not assume its in-process Python variables are durable memory.

---

## 3. The learning loop to use for every lab

Do not mark a lab complete just because a command succeeded.

Use this six-step loop:

### Step 1 — Explain it without code

Before running anything, answer:

- What problem are we solving?
- Which AgentCore service solves it?
- What would happen without that service?

### Step 2 — Draw the request path

Example:

```text
User -> Runtime -> Agent -> Gateway -> Lambda -> External API
                     |
                     +-> Model
```

If you cannot draw the request path, you do not yet understand the lab.

### Step 3 — Predict the result

Write down what you expect before running the command.

Examples:

- "A second request with the same session should see previous context."
- "A new session should not inherit in-process state."
- "The tool call should be denied by policy."
- "The trace should contain the model and tool spans."

### Step 4 — Run the example

Use the README and scripts in the lab folder.

### Step 5 — Prove it

Capture evidence:

- output,
- trace,
- memory record,
- Gateway tool list,
- policy decision,
- registry record,
- or evaluation result.

### Step 6 — Change one thing

Never finish a lab without changing something yourself.

Examples:

- add a second tool,
- use a different session ID,
- deny one action,
- change the memory actor,
- break the OAuth scope and diagnose it,
- add an evaluator,
- add a new registry record.

That final change converts a tutorial into learning.

---

## 4. Golden lab structure

When extending this repository, each lab should eventually follow this structure:

```text
1. What you will learn
2. Theory / mental model
3. Architecture / request flow
4. Important AgentCore concepts
5. Code walkthrough
6. Prerequisites
7. Run it
8. Expected result
9. Learner assignment
10. Success criteria
11. Common failures / troubleshooting
12. Production notes
13. Cleanup
```

The repository is moving toward this format. Older labs may still have shorter READMEs.

---

# 5. Lab-by-lab assignments

The assignments below are designed so an instructor can say, "Complete Part X," and the learner has a concrete outcome to produce.

## Phase A — Runtime fundamentals

### Part 03 — Simple Runtime agent

**Core question:** What does AgentCore Runtime do if there is no LLM, Memory, Gateway, or tool?

**Assignment:** Deploy the echo-style agent, invoke it twice, and explain the path from CLI request to the `@app.entrypoint` function and back.

**Change it:** Add a new deterministic command such as `health` that returns runtime/application metadata.

**Proof:** Show two invocation outputs and a short diagram:

```text
CLI -> Runtime -> entrypoint -> Python response -> CLI
```

### Part 04 — Runtime + foundation model

**Core question:** What changes when the Runtime-hosted application calls Bedrock Runtime?

**Assignment:** Compare Part 03 and Part 04. Identify exactly which lines introduce model inference.

**Change it:** Change the model or model parameters and explain the behavioral difference.

**Proof:** Capture a model response and identify the AgentCore call versus the Bedrock model call.

### Part 05 — Ephemeral in-process conversation state

**Core question:** Why is a Python dictionary/list not durable agent memory?

**Assignment:** Keep context in the same running environment, then start a fresh session/environment and observe what disappears.

**Change it:** Store a value in process memory and intentionally demonstrate its loss.

**Proof:** A before/after transcript plus an explanation of **ephemeral state vs AgentCore Memory**.

### Part 06 — External client

**Core question:** How does a real application invoke a Runtime instead of using only the CLI?

**Assignment:** Use the Python client and identify runtime ARN, session ID, payload, and response handling.

**Change it:** Accept the prompt from command-line input.

**Proof:** Run the same agent once through CLI and once through Python.

---

## Phase B — Memory

### Part 08 — Short-term Memory

**Core question:** What are `memory_id`, `actor_id`, `session_id`, and conversational `role`?

**Assignment:** Run two conversations for the same actor with two different session IDs. Confirm the histories remain logically separated.

**Change it:** Use two different actor IDs and explain why actor identity must not be confused with USER/ASSISTANT message roles.

**Proof:** Print/list the events for both actor/session combinations.

### Part 09 — Built-in long-term memory strategy

**Core question:** How are short-term events transformed into long-term records?

**Assignment:** Create a conversation containing durable facts/preferences and inspect the resulting long-term records.

**Change it:** Add information that should *not* be useful as long-term memory and compare what is extracted.

**Proof:** Show original events and extracted memory records.

### Part 11 — Self-managed long-term memory strategy

**Core question:** When would you control extraction/retrieval yourself rather than rely entirely on a built-in strategy?

**Assignment:** Trace the complete write -> extraction -> retrieval path.

**Change it:** Alter the custom extraction or storage logic for one new fact type.

**Proof:** Demonstrate one record created by your custom logic.

### Part 13 — Episodic memory

**Core question:** How is an "episode" different from a fact, preference, or conversation summary?

**Assignment:** Create two distinct task episodes and inspect what the strategy retains.

**Change it:** Repeat a similar task with a different outcome and compare the episodes.

**Proof:** Explain how the retrieved episode could improve a future decision.

---

## Phase C — Gateway and tool use

### Part 15 — Gateway -> Lambda tool

**Core question:** Why put a Gateway between an agent/client and a tool?

**Assignment:** Follow the chain from MCP request to Gateway target to Lambda.

**Change it:** Add one argument to the Lambda tool schema and implementation.

**Proof:** `list tools` shows the contract and `call tool` successfully invokes it.

### Part 16 — Container agent + OAuth + Gateway

**Core question:** How do Runtime hosting, OAuth, and Gateway fit together?

**Assignment:** Identify inbound Runtime authentication separately from outbound/tool authentication.

**Change it:** Use an invalid/insufficient OAuth scope and document the failure.

**Proof:** Successful tool call plus the expected authentication failure test.

### Part 17 — Python client calling containerized Runtime agent

**Core question:** Is the client coupled to the agent's packaging format?

**Assignment:** Invoke the deployed agent and explain why the caller should not care whether the implementation was container-packaged.

**Change it:** Reuse a session ID for multiple calls.

**Proof:** Client transcript and session behavior explanation.

### Part 18 — Real-time weather agent

**Core question:** How does an LLM decide to use a dynamically discovered tool?

**Assignment:** Trace:

```text
User -> Runtime -> LLM -> Gateway tool discovery -> Weather tool -> OpenWeather -> LLM -> User
```

**Change it:** Ask one prompt that needs weather and one that does not. Verify the tool is only required for the first.

**Proof:** Tool discovery/call evidence and final responses.

### Part 19 — Multi-tool Gateway

**Core question:** What changes when an agent has many tools?

**Assignment:** Enumerate tools, their contracts, and which prompt should select each one.

**Change it:** Add a second/third tool with intentionally overlapping wording and observe selection behavior.

**Proof:** Three prompts routing to the intended tools.

### Part 20 — Enterprise multi-tool orchestration

**Core question:** How do you keep orchestration code separate from tool implementations?

**Assignment:** Map orchestration decisions, Gateway calls, and client responsibilities.

**Change it:** Add a new business action without changing unrelated tools.

**Proof:** Architecture diagram and successful end-to-end invocation.

---

## Phase D — Identity

### Part 22 — Identity-governed research assistant

**Core question:** How can an agent act on behalf of a user without hardcoding user credentials?

**Assignment:** Trace where the OAuth token originates, who stores/brokers it, and where it is used.

**Change it:** Test a missing/revoked authorization case.

**Proof:** Successful governed access plus failure behavior when authorization is unavailable.

---

## Phase E — Managed tools

### Part 24 — Code Interpreter

**Core question:** Why execute generated code in a managed isolated tool instead of inside the main agent process?

**Assignment:** Ask for a calculation and a plot/data operation.

**Change it:** Give a problem where the model can answer directly and another where code execution improves reliability.

**Proof:** Tool execution result and explanation of the isolation boundary.

### Part 25 — Revenue intelligence

**Core question:** How do reasoning and deterministic analysis work together?

**Assignment:** Identify which steps should be done by the LLM and which should be done by Python.

**Change it:** Add a new KPI calculation.

**Proof:** Input data, generated computation, and final business explanation.

### Part 26 — Browser market intelligence

**Core question:** When is Browser a better fit than a simple HTTP/API tool?

**Assignment:** Trace browser session creation, navigation, extraction, and agent reasoning.

**Change it:** Research a second target with a different page structure.

**Proof:** Collected evidence and final synthesized answer.

### Part 27 — Browser form automation

**Core question:** What extra risks appear when an agent changes a website rather than only reading it?

**Assignment:** Identify every point at which a destructive/irreversible action could occur.

**Change it:** Add a confirmation checkpoint before the final submit action.

**Proof:** Demonstrate that navigation can proceed but submission waits for approval.

---

## Phase F — Observability and evaluation

### Part 30 — ADOT / AgentCore Observability

**Core question:** How do you debug a multi-step agent request?

**Assignment:** Execute one request and reconstruct it from traces.

**Change it:** Add one custom span or useful attribute.

**Proof:** A trace showing the important stages of the request.

### Part 36 — Evaluation enablement

**Core question:** Why do evaluations depend on good traces/instrumentation?

**Assignment:** Capture test interactions and explain which data an evaluator consumes.

**Change it:** Create two prompts: one expected to pass and one intentionally poor case.

**Proof:** Evaluation inputs/results linked back to the underlying trace.

### Part 38 — Model-as-judge evaluator

**Core question:** What are the strengths and weaknesses of using another model as an evaluator?

**Assignment:** Inspect the rubric and run it against clearly good/bad responses.

**Change it:** Modify one rubric criterion and see how results change.

**Proof:** Before/after evaluation results and a short discussion of evaluator subjectivity.

### Part 39 — Code evaluator

**Core question:** When is deterministic evaluation better than model-as-judge?

**Assignment:** Implement or modify a rule that can be objectively checked.

**Change it:** Add one boundary/edge case.

**Proof:** Passing and failing examples with deterministic reasons.

---

## Phase G — Policy/governance

### Part 32 — Policy enforcement

**Core question:** Where should authorization decisions happen when an agent wants to act?

**Assignment:** Demonstrate one allowed and one denied action.

**Change it:** Add a policy condition.

**Proof:** Same agent/tool path, different policy outcome.

### Part 33 — Multi-tool policy enforcement

**Core question:** How do policies behave when an agent can choose among multiple tools?

**Assignment:** Define which identity/context may call which tool.

**Change it:** Allow one tool while denying another for the same principal/session.

**Proof:** Tool-level authorization evidence.

---

## Phase H — Payments

### Part 41 — Payment infrastructure

**Core question:** What infrastructure is needed before an agent can perform payment-aware actions?

**Assignment:** Map the resources and trust boundaries.

**Change it:** Document which values are secrets, identifiers, and non-sensitive configuration.

**Proof:** Resource inventory and security boundary diagram.

### Part 42 — Payment + agent + Gateway integration

**Core question:** How is a commercial/payment action different from a normal tool call?

**Assignment:** Trace the payment-aware end-to-end request.

**Change it:** Add a failure scenario such as invalid/absent payment context.

**Proof:** Success and controlled failure outcomes.

---

## Phase I — Modern CLI and Registry

### Part 44 — Current AgentCore CLI concepts

**Core question:** What changed from the legacy Python Starter Toolkit to the current `@aws/agentcore` CLI?

**Assignment:** Install the current CLI and map the current commands (`create`, `dev`, `deploy`, `invoke`, etc.) to the old mental model.

**Change it:** Create a minimal current-CLI project independently of the legacy labs.

**Proof:** Local development invocation plus deployed invocation.

> This lab originated during the CLI preview period. Treat preview-era limitations in the folder as historical unless confirmed in current AWS docs.

### Part 46 — Registry publish

**Core question:** What does publishing a record give you that a hardcoded URL/ARN does not?

**Assignment:** Publish the MCP server record and inspect its metadata.

**Change it:** Add metadata that would help a client decide whether the resource is appropriate.

**Proof:** Registry lookup showing the published record.

### Part 47 — Programmatic Registry discovery

**Core question:** How can an agent/application discover capabilities dynamically?

**Assignment:** Perform the same discovery through the available programmatic approaches and compare the returned data.

**Change it:** Filter/search for a specific capability.

**Proof:** Program output selecting the intended record without a hardcoded runtime endpoint.

### Part 48 — Registry + Runtime + HITL capstone

**Core question:** How do discovery, execution, and human approval combine in a governed agent workflow?

**Assignment:** Draw and execute:

```text
Request
  -> Registry discovery
  -> choose approved agent/resource
  -> prepare action
  -> human approval
  -> Runtime invocation
  -> result
```

**Change it:** Add one operation that is read-only and does not need approval, plus one action that must require approval.

**Proof:** The read-only path proceeds; the action path pauses until approval.

---

# 6. Suggested capstone

After completing the labs, build one small production-shaped system instead of another isolated demo.

Example: **Cloud Operations Assistant**

```text
Engineer
   |
   v
Authenticated application
   |
   v
AgentCore Runtime
   |
   +--> Memory       : user/session preferences and durable context
   +--> Gateway      : approved cloud/ops tools
   +--> Identity     : user/delegated credentials
   +--> Policy       : deny dangerous operations unless conditions are met
   +--> Code Tool    : analyze logs/metrics
   +--> Browser      : optional web-console/document workflow
   +--> Observability: full traces
   +--> Evaluations  : correctness + safety checks
   +--> Registry     : discover approved tools/agents
```

Required behaviors:

1. Answer a read-only infrastructure question.
2. Use a Gateway tool.
3. Store/retrieve useful context.
4. Deny at least one unsafe action through policy.
5. Require human confirmation before one state-changing action.
6. Produce a trace that explains the execution.
7. Run at least one deterministic evaluator and one semantic/model-based evaluator.
8. Document what is demo-grade versus production-grade.

---

# 7. What "I understand AgentCore" should mean

A learner is ready to move beyond the tutorial when they can answer these without looking at the code:

- What does Runtime manage?
- What is isolated by a Runtime session?
- What disappears when ephemeral compute ends?
- When should I use AgentCore Memory?
- What is the difference between `actor_id`, `session_id`, and message role?
- Why would I put a tool behind Gateway?
- Where does Identity fit for inbound versus outbound access?
- Why use Code Interpreter or Browser instead of running everything inside the agent?
- How do I see what an agent actually did?
- Where should policy enforcement happen?
- How do I test agent quality continuously?
- Why use a Registry instead of hardcoding every agent/tool endpoint?
- Where should a human approval step be inserted?

If the learner can both **explain those answers and demonstrate them using the labs**, the repository has done its job.
