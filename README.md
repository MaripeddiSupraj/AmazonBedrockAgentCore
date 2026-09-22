# Amazon Bedrock AgentCore — Hands-On Labs

A collection of 31 self-contained, hands-on labs for [Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/) — AWS's managed platform for deploying, running, and governing AI agents in production. Each lab is a standalone folder with its own agent code, IAM policies, and setup commands, walking through one AgentCore capability at a time: Runtime, Memory, Gateway, Identity, Code Interpreter, Browser, Observability, Policy, Payments, Evaluations, and the Agent Registry.

This is a **learning repo, not a production template** — every lab optimizes for showing one concept clearly, not for hardening. Treat the code as a starting point and apply your own security review before running anything against a real AWS account with production access.

## Who this is for

Cloud/DevOps/platform engineers who already know AWS (IAM, Lambda, ECR, Secrets Manager) and want a guided, incremental path into building agents on Bedrock AgentCore — from a one-file "hello world" agent up to identity-governed, policy-enforced, evaluated, paid agent-to-agent workflows.

## How the labs are organized

Every `part-NN-*` folder follows the same shape (not every lab needs every piece):

```
part-NN-lab-name/
├── README.md          # what this lab demonstrates, prerequisites, how to run it
├── agent/              # the agent's application code (app.py / Dockerfile / requirements.txt)
├── policies/           # IAM policy / trust policy JSON for this lab's execution role
├── commands/ or setup/ # the exact CLI commands / shell scripts used to stand it up
├── gateway/, lambda/    # Gateway schema + the Lambda tool behind it, where relevant
└── client/              # an external caller for the deployed agent, where relevant
```

Start at Part 3 and work forward — later labs assume the Gateway, Memory, or Identity resources built in earlier ones.

| Part | Lab | AgentCore capability |
|---|---|---|
| [03](part-03-deploy-a-simple-agent-with-starter-toolkit/) | Deploy a Simple Agent with the Starter Toolkit | Runtime |
| [04](part-04-deploy-a-llm-agent-with-starter-toolkit/) | Deploy an LLM Agent with the Starter Toolkit | Runtime |
| [05](part-05-deploy-an-ephemeral-memory-agent/) | Deploy an Ephemeral Memory Agent | Runtime |
| [06](part-06-create-a-python-client-to-chat-with-an-empheral-agent/) | Create a Python Client to Chat with an Ephemeral Agent | Runtime |
| [08](part-08-deploy-a-short-term-memory-agent/) | Deploy a Short-Term Memory Agent | Memory |
| [09](part-09-long-term-memory-with-builtin-strategies/) | Long-Term Memory with Built-In Strategies | Memory |
| [11](part-11-ltm-with-self-managed-strategy/) | Long-Term Memory with a Self-Managed Strategy | Memory |
| [13](part-13-long-term-memory-with-built-in-episodic-strategy/) | Long-Term Memory with the Built-In Episodic Strategy | Memory |
| [15](part-15-gateway-calling-a-lambda-tool/) | Gateway Calling a Lambda Tool | Gateway |
| [16](part-16-docker-based-agent-with-oauth-gateway-lambda-tool/) | Docker-Based Agent with OAuth Gateway & Lambda Tool | Runtime + Gateway |
| [17](part-17-calling-an-agentcore-docker-agent-from-a-python-client/) | Calling an AgentCore Docker Agent from a Python Client | Runtime |
| [18](part-18-real-time-weather-agent-with-agentcore-llm-oauth-and-openweather-api/) | Real-Time Weather Agent with AgentCore, LLM, OAuth and OpenWeather API | Runtime + Gateway + Identity |
| [19](part-19-multi-tool-gateway/) | Multi-Tool Gateway | Gateway |
| [20](part-20-orchestrating-enterprise-ai-agents-multi-tool-gateway-and-client-integration/) | Orchestrating Enterprise AI Agents: Multi-Tool Gateway and Client Integration | Runtime + Gateway |
| [22](part-22-identity-governed-ai-research-assistant-for-investment-analysis/) | Identity-Governed AI Research Assistant for Investment Analysis | Identity + Gateway |
| [24](part-24-code-interpreter-build-an-ai-agent-that-writes-and-executes-code/) | Code Interpreter — Build an AI Agent That Writes and Executes Code | Code Interpreter |
| [25](part-25-from-data-to-decisions-building-an-ai-revenue-intelligence-agent/) | From Data to Decisions: Building an AI Revenue Intelligence Agent | Code Interpreter |
| [26](part-26-from-queries-to-insights-building-an-ai-market-intelligence-agent-with-bt/) | From Queries to Insights: Building an AI Market Intelligence Agent with the Browser Tool | Browser |
| [27](part-27-from-insights-to-action-live-form-automation-with-ai-agents/) | From Insights to Action: Live Form Automation with AI Agents | Browser (Playwright) |
| [30](part-30-from-insights-to-visibility-monitoring-your-market-intelligence-agent-with-adot/) | From Insights to Visibility: Monitoring Your Market Intelligence Agent with ADOT | Observability |
| [32](part-32-policy-enforcement/) | Policy Enforcement | Policy |
| [33](part-33-multitool-gateway-policy-enforcement/) | Multitool Gateway Policy Enforcement | Policy |
| [36](part-36-agent-evaluation-enablement-with-langchain-langgraph/) | Agent Evaluation Enablement with LangChain + LangGraph | Evaluations + Observability |
| [38](part-38-custom-evaluator-model-as-judge/) | Custom Evaluator: Model-as-Judge | Evaluations |
| [39](part-39-custom-code-evaluators/) | Custom Code Evaluators | Evaluations |
| [41](part-41-payment-infrastructure-setup/) | Payment Infrastructure Setup | Payments |
| [42](part-42-payments-agent-gateway-integration/) | Payments, Agent & Gateway Integration | Payments + Gateway |
| [44](part-44-agentcore-cli-preview-installation-and-current-limitations/) | AgentCore CLI Preview: Installation and Current Limitations | Tooling |
| [46](part-46-create-your-first-registry-publish-a-mcp-server-record/) | Create Your First Registry & Publish an MCP Server Record | Registry |
| [47](part-47-programmatic-registry-discovery-aws-sdk-mcp/) | Programmatic Registry Discovery: AWS SDK + MCP | Registry |
| [48](part-48-hitl-agent-execution-after-registry-discovery/) | HITL Agent Execution After Registry Discovery | Registry + Runtime |

Part numbers skip around (no 1–2, 7, 10, 12, 14, 21...) — those were either conceptual/no-code write-ups or not included in this snapshot of the series.

## Prerequisites

- An AWS account with **Amazon Bedrock AgentCore** enabled, and model access granted for the Claude models used (`bedrock-runtime`)
- Python 3.11+ and `pip`
- Docker, for the labs that build a container image (most Runtime labs from Part 16 onward)
- The AWS CLI, configured with credentials that can create IAM roles, Lambda functions, ECR repos, and AgentCore resources
- For the CLI itself, two generations are used across this repo — check each lab's README for which one it expects:
  - **Parts 3–20ish**: the Python `bedrock-agentcore-starter-toolkit` (`agentcore configure` / `launch` / `invoke`)
  - **Part 44 onward**: the newer, npm-distributed preview CLI (`npm install -g @aws/agentcore`, then `agentcore create` / `dev` / `deploy`)
  - Always cross-check command syntax against the [current AgentCore CLI docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-get-started-cli.html) and [release notes](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/release-notes.html) — this is a fast-moving preview product and commands have changed between when a lab was written and when you run it.

Every `requirements.txt` in this repo pins `bedrock-agentcore` differently (`0.1.7` in the earliest labs, unpinned or `>=1.18.0` in the newest) because the SDK moved fast over the life of this series. If a lab fails to install or run, check its pinned version against the [PyPI release history](https://pypi.org/project/bedrock-agentcore/) first.

## Before you deploy anything

Every lab uses placeholder values (`<<ACCOUNT ID>>`, `<YOUR_API_KEY>`, `123456789012`, etc.) for account IDs, ARNs, and API keys — replace them with your own before running. None of the IAM policies in `policies/` folders are least-privilege by default; review and scope them down before using this against anything beyond a personal sandbox account.

## License

[MIT](LICENSE) — see the LICENSE file. The IAM policy JSON, Cedar policies, and setup scripts are provided as-is; review them against your own security requirements before use.

## Attribution

This repo grew out of an Amazon Bedrock AgentCore tutorial series. If you're building on it publicly, please keep the license and attribution intact.
