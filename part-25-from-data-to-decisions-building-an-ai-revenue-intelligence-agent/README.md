# Part 25 — From Data to Decisions: Building an AI Revenue Intelligence Agent

**AgentCore capability:** Code Interpreter

Points the Code Interpreter at real data in S3 (see `sample-data/Sample Data.zip`) with "public network" mode enabled so it can pull the file, then analyzes it for revenue trends and summarizes the findings — a template for a self-serve analytics agent.

## Prerequisites

- An S3 bucket with CORS configured (`policies/S3CORSpolicy.json`)
- A Code Interpreter custom tool ID with public network mode enabled

## Run it

1. Upload `sample-data/Sample Data.zip` (unzipped) to your S3 bucket
2. `bash agent/deploy.sh`, deploy as a Runtime agent
3. Give it an S3 URI and ask for a summary

---

[← Back to the lab index](../README.md)
