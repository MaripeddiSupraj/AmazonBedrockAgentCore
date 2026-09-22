# Part 42 — Payments, Agent & Gateway Integration

**AgentCore capability:** Payments + Gateway

Wires the Part 41 payment instrument into an agent that calls a paid tool through the Gateway, using `PAYMENT_MANAGER_ARN` / `PAYMENT_INSTRUMENT_ID` env vars. `troubleshooting/Curl Command.txt` documents a duplicate `Set-Cookie` header issue hit while testing against a real x402 discovery endpoint — left in as a real-world debugging note.

## Prerequisites

- A payment instrument from Part 41
- A Gateway tool that requires payment

## Run it

1. Set the payment env vars in `agent/deploy.sh` / the Runtime configuration
2. `bash agent/deploy.sh`, deploy as a Runtime agent
3. See `troubleshooting/Curl Command.txt` if you hit cookie/session errors against the paid endpoint

---

[← Back to the lab index](../README.md)
