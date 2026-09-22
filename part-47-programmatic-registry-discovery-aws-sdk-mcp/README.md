# Part 47 — Programmatic Registry Discovery: AWS SDK + MCP

**AgentCore capability:** Registry

Two different ways to query the Part 46 registry programmatically: `discovery/mcpdiscovery.py` talks to the registry's MCP endpoint directly with hand-rolled SigV4-signed JSON-RPC calls, while `discovery/awssdkdiscovery.py` does the same thing through the AWS SDK — useful for seeing both the low-level protocol and the ergonomic path.

## Prerequisites

- The registry record from Part 46 published
- An IAM role/user with registry read access (`policies/`)

## Run it

1. `python discovery/mcpdiscovery.py`
2. `python discovery/awssdkdiscovery.py`
3. Compare the two outputs

---

[← Back to the lab index](../README.md)
