# Amazon Bedrock AgentCore — Hands-On Labs

A hands-on learning repository for [Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/) — AWS's managed platform for deploying, running, and governing AI agents.

The repository contains **31 feature labs** covering Runtime, Memory, Gateway, Identity, Code Interpreter, Browser, Observability, Policy, Payments, Evaluations, and the Agent Registry.

> **New learner? Start with [course/](course/README.md).** Days 1–5 are the current, teaching-first reference: one concept per day, minimal code, visual request flows, prediction exercises, failure experiments, assignments, and explain-back tests. After Day 5, use [LEARNING_GUIDE.md](LEARNING_GUIDE.md) and the `part-*` labs to continue deeper into AgentCore capabilities.

The older `part-*` folders remain valuable feature examples and historical implementation references, but they are no longer the recommended first five lessons.

This is a **learning repo, not a production template**. Each lab optimizes for explaining one concept. Review IAM, secrets, networking, model choices, dependency versions, observability, failure handling, and security controls before adapting any example to production.

---

## What this repo is designed to teach

The goal is not only:

> "I ran the command and the agent responded."

The goal is:

> "I understand what AgentCore component is involved, why it is needed, what happens behind the scenes, which code is responsible, and how to prove the behavior."

Use every lab in this order:

```text
Theory
  -> architecture / request flow
  -> predict the behavior
  -> run the example
  -> verify the result
  -> change one thing yourself
```

The detailed learning loop and all lab assignments are in [LEARNING_GUIDE.md](LEARNING_GUIDE.md).

---

## Important CLI note — current vs legacy examples

AgentCore has changed significantly during the lifetime of this tutorial series.

### Current recommendation for new projects

AWS currently recommends the npm-distributed **AgentCore CLI**:

```bash
npm install -g @aws/agentcore
```

Typical current workflow:

```text
agentcore create
agentcore dev
agentcore deploy
agentcore invoke
```

### Legacy labs in this repository

Many earlier labs were written with the Python **`bedrock-agentcore-starter-toolkit`**, which uses commands such as:

```text
agentcore configure
agentcore launch
agentcore invoke
```

The Starter Toolkit is now a **legacy/unsupported starting point for new projects**. These labs remain valuable for understanding AgentCore concepts and SDK behavior, but do not assume every old deployment command is the current recommended workflow.

**Rule for learners:** understand the concept from the lab, then compare deployment commands against the current AWS AgentCore documentation.

---

## Who this is for

Best suited to:

- Cloud / DevOps / Platform engineers
- AI platform engineers
- application developers learning production agent infrastructure
- engineers who already understand basic AWS concepts such as IAM, Lambda, ECR, Secrets Manager, and API authentication

You do **not** need to be an expert in agent frameworks before starting. The early labs intentionally separate Runtime behavior from LLM/tool/memory behavior.

---

## AgentCore mental model

| Capability | Simple mental model | What it solves |
|---|---|---|
| **Runtime** | Where the agent runs | managed execution, scaling, session isolation |
| **Memory** | What the agent remembers | short-term events and durable learned context |
| **Gateway** | Controlled front door to tools | expose APIs/Lambda/tools through MCP |
| **Identity** | Who is calling / which credentials may be used | inbound and outbound auth |
| **Code Interpreter** | Managed code execution room | calculations, analysis, generated code |
| **Browser** | Managed browser | browsing and web automation |
| **Observability** | Flight recorder | traces, logs, metrics |
| **Policy** | Action authorization layer | allow/deny agent tool actions |
| **Evaluations** | Quality test system | measure agent behavior |
| **Registry** | Catalog | discover approved agents/tools/resources |
| **Payments** | Commercial action plumbing | payment-aware agent workflows |

Read the deeper explanation in [LEARNING_GUIDE.md](LEARNING_GUIDE.md).

---

## The two flows to understand first

### Deployment

For modern projects:

```text
Agent source
   |
   v
agentcore dev
   |
   v
agentcore deploy
   |
   v
AgentCore Runtime deployment
```

Older labs may use:

```text
agentcore configure
   |
   v
agentcore launch
   |
   v
AgentCore Runtime deployment
```

### Invocation

```text
Client
  |
  | payload + session
  v
AgentCore Runtime
  |
  v
Agent application
  |
  +--> Model
  +--> Memory
  +--> Gateway / tools
  +--> Browser / Code Interpreter
  |
  v
Response
```

A Runtime session is **not the same thing as AgentCore Memory**. Runtime execution state is ephemeral unless you intentionally persist it. Memory is a separate service for durable agent context.

---

## How the labs are organized

Every `part-NN-*` folder follows roughly this shape:

```text
part-NN-lab-name/
├── README.md          # what this lab demonstrates and how to run it
├── agent/             # application code
├── policies/          # IAM policy / trust policy examples
├── commands/ or setup/# CLI commands / setup scripts
├── gateway/, lambda/  # Gateway schema + target implementation where relevant
├── client/            # external caller where relevant
└── utils/             # inspection/testing helpers where relevant
```

Not every lab needs every folder.

The repository is progressively moving toward a stronger teaching format:

```text
What -> Why -> Architecture -> Code -> Run -> Expected Result
     -> Assignment -> Success Criteria -> Troubleshooting -> Production Notes
```

---

## Recommended learning order

### Phase A — Runtime fundamentals

| Part | Lab | Capability |
|---|---|---|
| [03](part-03-deploy-a-simple-agent-with-starter-toolkit/) | Deploy a Simple Agent with the Starter Toolkit | Runtime |
| [04](part-04-deploy-a-llm-agent-with-starter-toolkit/) | Deploy an LLM Agent with the Starter Toolkit | Runtime |
| [05](part-05-deploy-an-ephemeral-memory-agent/) | Deploy an Ephemeral Memory Agent | Runtime |
| [06](part-06-create-a-python-client-to-chat-with-an-empheral-agent/) | Create a Python Client to Chat with an Ephemeral Agent | Runtime |

### Phase B — Memory

| Part | Lab | Capability |
|---|---|---|
| [08](part-08-deploy-a-short-term-memory-agent/) | Deploy a Short-Term Memory Agent | Memory |
| [09](part-09-long-term-memory-with-builtin-strategies/) | Long-Term Memory with Built-In Strategies | Memory |
| [11](part-11-ltm-with-self-managed-strategy/) | Long-Term Memory with a Self-Managed Strategy | Memory |
| [13](part-13-long-term-memory-with-built-in-episodic-strategy/) | Long-Term Memory with the Built-In Episodic Strategy | Memory |

### Phase C — Gateway, tools, and Identity

| Part | Lab | Capability |
|---|---|---|
| [15](part-15-gateway-calling-a-lambda-tool/) | Gateway Calling a Lambda Tool | Gateway |
| [16](part-16-docker-based-agent-with-oauth-gateway-lambda-tool/) | Docker-Based Agent with OAuth Gateway & Lambda Tool | Runtime + Gateway |
| [17](part-17-calling-an-agentcore-docker-agent-from-a-python-client/) | Calling an AgentCore Docker Agent from a Python Client | Runtime |
| [18](part-18-real-time-weather-agent-with-agentcore-llm-oauth-and-openweather-api/) | Real-Time Weather Agent with AgentCore, LLM, OAuth and OpenWeather API | Runtime + Gateway + Identity |
| [19](part-19-multi-tool-gateway/) | Multi-Tool Gateway | Gateway |
| [20](part-20-orchestrating-enterprise-ai-agents-multi-tool-gateway-and-client-integration/) | Orchestrating Enterprise AI Agents | Runtime + Gateway |
| [22](part-22-identity-governed-ai-research-assistant-for-investment-analysis/) | Identity-Governed AI Research Assistant | Identity + Gateway |

### Phase D — Managed tools

| Part | Lab | Capability |
|---|---|---|
| [24](part-24-code-interpreter-build-an-ai-agent-that-writes-and-executes-code/) | Code Interpreter — Build an AI Agent That Writes and Executes Code | Code Interpreter |
| [25](part-25-from-data-to-decisions-building-an-ai-revenue-intelligence-agent/) | From Data to Decisions: Revenue Intelligence | Code Interpreter |
| [26](part-26-from-queries-to-insights-building-an-ai-market-intelligence-agent-with-bt/) | Market Intelligence Agent with Browser | Browser |
| [27](part-27-from-insights-to-action-live-form-automation-with-ai-agents/) | Live Form Automation with AI Agents | Browser (Playwright) |

### Phase E — Operability, policy, and evaluation

| Part | Lab | Capability |
|---|---|---|
| [30](part-30-from-insights-to-visibility-monitoring-your-market-intelligence-agent-with-adot/) | Monitoring with ADOT | Observability |
| [32](part-32-policy-enforcement/) | Policy Enforcement | Policy |
| [33](part-33-multitool-gateway-policy-enforcement/) | Multitool Gateway Policy Enforcement | Policy |
| [36](part-36-agent-evaluation-enablement-with-langchain-langgraph/) | Agent Evaluation Enablement with LangChain + LangGraph | Evaluations + Observability |
| [38](part-38-custom-evaluator-model-as-judge/) | Custom Evaluator: Model-as-Judge | Evaluations |
| [39](part-39-custom-code-evaluators/) | Custom Code Evaluators | Evaluations |

### Phase F — Payments and discovery

| Part | Lab | Capability |
|---|---|---|
| [41](part-41-payment-infrastructure-setup/) | Payment Infrastructure Setup | Payments |
| [42](part-42-payments-agent-gateway-integration/) | Payments, Agent & Gateway Integration | Payments + Gateway |
| [44](part-44-agentcore-cli-preview-installation-and-current-limitations/) | AgentCore CLI evolution / modern CLI | Tooling |
| [46](part-46-create-your-first-registry-publish-a-mcp-server-record/) | Create a Registry & Publish an MCP Server Record | Registry |
| [47](part-47-programmatic-registry-discovery-aws-sdk-mcp/) | Programmatic Registry Discovery | Registry |
| [48](part-48-hitl-agent-execution-after-registry-discovery/) | HITL Agent Execution After Registry Discovery | Registry + Runtime |

Part numbers skip because some original tutorial episodes were conceptual/no-code material and are not included in this repository snapshot.

---

## Prerequisites

At a minimum:

- AWS account in a Region where the required AgentCore capabilities are available
- Python 3.11+ for the Python labs
- AWS CLI with sandbox/development credentials
- Node.js/npm for the current `@aws/agentcore` CLI
- Docker/Finch/Podman for labs that explicitly require a local/container build
- appropriate Bedrock model access where a lab calls a foundation model
- permission to create the AWS resources used by the selected lab

Before starting:

```bash
aws sts get-caller-identity
```

Confirm that the returned account and identity are the sandbox/development account you intend to use.

---

## Version awareness

This repository spans multiple AgentCore generations.

You will see differences in:

- CLI names and flags
- Runtime deployment patterns
- SDK versions
- model IDs
- Memory helpers
- Gateway/Identity APIs

That is intentional history, but it can be confusing for a new learner.

When the lab and current documentation disagree:

1. keep the **concept** from the lab,
2. prefer the **current AWS command/API**,
3. record the difference in your learning notes.

---

## Security warning

The repository contains educational IAM policies and setup scripts.

Before running:

- replace placeholders such as `<<ACCOUNT ID>>`, `123456789012`, and `<YOUR_API_KEY>`
- do not commit secrets
- do not use production credentials
- scope IAM permissions down
- understand which resources incur cost
- clean up resources after each lab

Many policies are deliberately broad enough to make a learning exercise easy to follow. That does **not** make them appropriate for production.

---

## What counts as completing a lab?

A lab is complete only when you can produce all four:

1. **Explanation** — what and why
2. **Diagram** — request/data flow
3. **Evidence** — output/trace/memory/tool/policy/evaluation result
4. **Modification** — one change you made yourself

The specific assignment for every lab is in [LEARNING_GUIDE.md](LEARNING_GUIDE.md).

---

## License

[MIT](LICENSE).

## Attribution

This repository grew out of an Amazon Bedrock AgentCore tutorial series. If you build on it publicly, keep the license and attribution intact.
