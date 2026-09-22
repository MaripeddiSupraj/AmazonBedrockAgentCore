# Part 22 — Identity-Governed AI Research Assistant for Investment Analysis

**AgentCore capability:** Identity + Gateway

Uses AgentCore Identity (`bedrock_agentcore.services.identity.IdentityClient`) to broker Google OAuth tokens on the agent's behalf, then reasons over real quarterly earnings PDFs (`reports/`, Meta and Alphabet Q4 releases) to answer investment-research questions — a worked example of identity-governed access to a third-party service from inside an agent.

## Prerequisites

- A Google OAuth client registered with AgentCore Identity
- A Secrets Manager secret for the stored Google tokens (`GOOGLE_TOKENS_SECRET_ID`)

## Run it

1. `bash setup/Pythonsetup.sh && bash setup/Envsetup.sh`
2. `bash agent/deploy.sh`, deploy as a Runtime agent
3. Ask it questions about the PDFs in `reports/`

---

[← Back to the lab index](../README.md)
