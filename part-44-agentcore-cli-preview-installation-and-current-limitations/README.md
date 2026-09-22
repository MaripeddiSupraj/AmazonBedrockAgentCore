# Part 44 — AgentCore CLI: From Preview-Era Lab to the Current Workflow

**AgentCore capability:** Tooling

This folder was originally created while the npm-distributed AgentCore CLI was still being treated as a preview/new-generation tool in this tutorial series.

As of **September 2026**, the important update for learners is:

> The `@aws/agentcore` CLI is the recommended starting point for new AgentCore projects. The older Python `bedrock-agentcore-starter-toolkit` used by many earlier labs is a legacy path.

The folder name is intentionally preserved so existing links/history do not break.

---

## 1. Why this lab matters

If you completed Parts 03–20, you saw commands such as:

```text
agentcore configure
agentcore launch
agentcore invoke
```

Those belong to the older Starter Toolkit generation.

For new projects, think in terms of the current CLI workflow:

```text
agentcore create
      |
      v
agentcore dev
      |
      v
agentcore deploy
      |
      v
agentcore invoke
```

Do not confuse a change in CLI UX with a change in the core AgentCore concepts.

Runtime is still Runtime.
Memory is still Memory.
Gateway is still Gateway.

The CLI is the developer interface used to configure and manage those capabilities.

---

## 2. Install

```bash
npm install -g @aws/agentcore
agentcore --version
agentcore --help
```

Also verify your AWS identity:

```bash
aws sts get-caller-identity
```

---

## 3. Mental model

### `agentcore create`

Start/scaffold/import an AgentCore project.

Think:

> Create the local project/configuration that AgentCore tooling understands.

### `agentcore dev`

Run the development workflow locally.

Think:

> Fast local feedback before I create/update the cloud deployment.

### `agentcore deploy`

Deploy/update the agent and required AgentCore/AWS resources.

Think:

> Turn my local agent project into a managed cloud deployment.

### `agentcore invoke`

Send an invocation to the deployed Runtime.

Think:

> Execute the deployed agent with a payload/session.

Other current CLI capabilities can manage or inspect resources such as logs, traces, evaluations, Gateway, and Memory. Use `agentcore --help` and current AWS documentation because the command surface continues to evolve.

---

## 4. Deployment vs invocation

Do not mix these two flows.

### Deployment

```text
source/config
   |
   v
agentcore deploy
   |
   v
Runtime version/endpoint + supporting configuration
```

### Invocation

```text
client/CLI
   |
   | prompt + session
   v
deployed Runtime
   |
   v
agent code
   |
   v
response
```

Deployment creates/updates something that can run.
Invocation asks the deployed thing to do work.

---

## 5. The file in this lab

`main.py` is intentionally minimal.

Read it before running anything and identify:

- the Runtime application object,
- the entrypoint/handler,
- the payload shape,
- the returned response.

The small codebase is useful because CLI behavior is the focus of this lab.

---

## 6. Run it

Start by checking the current CLI:

```bash
agentcore --version
agentcore --help
```

Then use the current documented project flow.

A typical learning sequence is:

```text
create/import project
     ->
agentcore dev
     ->
local invocation/test
     ->
agentcore deploy
     ->
agentcore invoke
```

Exact flags can change. Prefer the current CLI help and AWS documentation over old screenshots/tutorial commands.

---

## 7. Learner assignment

Create a tiny new agent using the current CLI rather than reusing only the old Starter Toolkit labs.

Your agent needs two deterministic behaviors:

```text
health  -> confirms the application runs
echo    -> returns supplied input
```

Then demonstrate:

1. local development behavior with `agentcore dev`,
2. cloud deployment with `agentcore deploy`,
3. remote execution with `agentcore invoke`.

---

## 8. Success criteria

You should be able to explain:

```text
legacy Starter Toolkit        current AgentCore CLI
----------------------        ---------------------
configure                     create/configuration workflow
launch                        deploy
invoke                        invoke
local launch variants         dev / current local workflow
```

This is a **mental mapping**, not a promise that every old flag has a one-to-one modern replacement.

---

## 9. Historical limitations

Any notes/scripts in this folder that describe a feature as "preview", "unsupported", or "currently missing" represent the state of the CLI when that tutorial episode was created.

Before repeating such a claim today:

1. run `agentcore --help`,
2. read the current AgentCore CLI documentation,
3. check current release notes.

Treat old limitations as historical evidence, not current product truth.

---

[← Back to the lab index](../README.md) · [Learning guide](../LEARNING_GUIDE.md)
