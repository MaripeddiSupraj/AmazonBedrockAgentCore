# Part 32 — Policy Enforcement

**AgentCore capability:** Policy

Config-only lab (no app code): a Cedar policy (`Cedar Policy.cedar`) that restricts a single Gateway tool call (LocationIQ geocoding) to only accept requests where the city is "Chicago", plus the plain-English-to-Cedar prompts used to draft it (`Cedar Policy NLP.txt`) and the script that associates the policy engine with the Gateway (`Policy Gateway Asso.sh`).

## Prerequisites

- A Gateway with a policy engine attached

## Run it

1. Review `Cedar Policy NLP.txt` for how the policy was reasoned about in plain English
2. `bash 'Policy Gateway Asso.sh'` to associate the policy with your Gateway
3. Call the tool with city=Chicago (allowed) vs. any other city (denied) to confirm enforcement

---

[← Back to the lab index](../README.md)
