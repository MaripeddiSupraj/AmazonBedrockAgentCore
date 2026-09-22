# Day 02 — Runtime + Foundation Model

## Today’s question

> If AgentCore Runtime runs my application, what service actually generates the LLM answer?

---

## Why should I care?

A common beginner mistake is to think:

```text
AgentCore Runtime = Bedrock model
```

They are different layers.

Today we add exactly one new component to Day 1:

```text
Runtime -> Amazon Bedrock model
```

This distinction matters later when debugging permissions, latency, model errors, Memory, and tools.

---

## One-sentence mental model

> **AgentCore Runtime hosts your Python application; Amazon Bedrock Runtime performs model inference when your application calls it.**

---

## Build on yesterday

### Day 1

```text
Client -> AgentCore Runtime -> Python -> response
```

### Day 2

```text
Client
  |
  v
AgentCore Runtime
  |
  v
Python handler
  |
  | bedrock.converse(...)
  v
Amazon Bedrock Runtime
  |
  v
Foundation model
  |
  v
Python handler
  |
  v
Client
```

The new arrow is:

```text
Python -> Bedrock model
```

---

## Architecture / request flow

```text
"Explain containers simply"
            |
            v
+--------------------------+
| AgentCore Runtime        |
| hosts main.py            |
+------------+-------------+
             |
             v
      handler(request)
             |
             | boto3 bedrock-runtime
             | Converse API
             v
+--------------------------+
| Amazon Bedrock Runtime   |
| invokes MODEL_ID         |
+------------+-------------+
             |
             v
      model-generated text
             |
             v
      handler returns JSON
```

### Responsibility map

| Layer | Responsibility |
|---|---|
| AgentCore Runtime | host/isolate/run the application |
| your handler | decide when/how to call the model |
| Bedrock Runtime | execute model inference |
| foundation model | generate the answer |

---

## Important terms

### Model ID

Identifies the Bedrock model or inference profile to use.

This course reads it from:

```text
MODEL_ID
```

instead of hardcoding a model that may later become outdated.

### Converse API

A Bedrock API that gives supported message-based models a common request shape.

That is easier to teach than starting with a different JSON schema for every model family.

### Inference configuration

Parameters such as maximum output tokens and temperature.

Do not spend Day 2 tuning them deeply. The goal is understanding the service boundary.

---

## Read the code

Open [main.py](main.py).

### 1. Runtime application

Same as Day 1:

```python
app = BedrockAgentCoreApp()
```

### 2. Bedrock Runtime client

New today:

```python
bedrock = boto3.client("bedrock-runtime", region_name=REGION)
```

This is **not** the AgentCore Runtime client.

### 3. Model call

```python
response = bedrock.converse(
    modelId=MODEL_ID,
    messages=[...],
)
```

That line crosses from your hosted agent application into model inference.

### 4. Response labels

The sample deliberately returns:

```json
{
  "hosted_by": "agentcore-runtime",
  "inference_by": "bedrock-runtime"
}
```

Those labels are educational. They make the two layers visible.

---

## Predict before running

### Prediction A

Run the same prompt twice.

Will the wording always be byte-for-byte identical?

**Expected:** not necessarily. A model is probabilistic.

### Prediction B

Set `MODEL_ID` to a nonexistent model.

Will AgentCore Runtime itself disappear?

**Expected:** no. The application can start, but the model call should fail.

### Prediction C

Remove the Bedrock call and return a fixed string.

Is it still an AgentCore Runtime application?

**Expected:** yes. Day 1 already proved that.

### Prediction D

Set `MODEL_ID` only in your terminal, but do not add it to the deployed Runtime configuration.

What should the cloud agent see?

**Expected:** the deployed process should not rely on your laptop's shell environment. Runtime configuration must be supplied to the deployment.

---

## Run it

Create a project:

```bash
agentcore create --name Day02Model --framework Strands --model-provider Bedrock --memory none --build CodeZip --protocol HTTP
cd Day02Model
```

Replace:

```text
app/Day02Model/main.py
```

with this day’s [main.py](main.py).

Choose a Bedrock model or inference profile that is available in your account and Region.

### Local development configuration

Put the model ID in:

```text
agentcore/.env.local
```

For example:

```text
MODEL_ID=<YOUR_SUPPORTED_MODEL_ID_OR_INFERENCE_PROFILE>
```

The current CLI loads local development variables from the project environment configuration.

### Deployed Runtime configuration

An exported shell variable on your laptop does **not** automatically become a deployed Runtime variable.

Open:

```text
agentcore/agentcore.json
```

and add `MODEL_ID` to the Day02Model runtime's `envVars`:

```json
"envVars": [
  {
    "name": "MODEL_ID",
    "value": "<YOUR_SUPPORTED_MODEL_ID_OR_INFERENCE_PROFILE>"
  }
]
```

This is intentionally visible in the lesson: **local process configuration and deployed Runtime configuration are different things.**

For the local development server:

```bash
agentcore dev
```

Then:

```bash
agentcore dev "Explain containers in exactly three short bullets."
```

Deploy:

```bash
agentcore deploy
```

Invoke:

```bash
agentcore invoke "Explain containers in exactly three short bullets."
```

---

## Expected evidence

The important evidence is not the exact model wording.

You should observe:

1. a generated answer,
2. the configured `model_id`,
3. `hosted_by = agentcore-runtime`,
4. `inference_by = bedrock-runtime`.

That proves the two-layer call path.

---

## Break it on purpose

Temporarily set:

```bash
export MODEL_ID="this-model-does-not-exist"
```

Invoke again.

### What should you learn?

A request can successfully reach your Runtime application and still fail at the **model inference layer**.

Later, this same debugging method will help you separate:

```text
Runtime problem?
Model problem?
Memory problem?
Gateway/tool problem?
```

Restore a valid model afterward.

---

## Learner assignment

Add a system instruction so the model behaves like a concise technical tutor.

For example, update the `converse` call with a system message appropriate for the current API.

Then test these two prompts:

```text
Explain Docker.
Explain Docker to a 10-year-old.
```

Capture the outputs and explain:

- what changed because of the user prompt,
- what changed because of your system instruction,
- what remained AgentCore Runtime responsibility.

---

## Explain-back test

Without looking at the code:

1. What is the difference between AgentCore Runtime and Bedrock Runtime?
2. Which line actually invokes the model?
3. Why do we use `MODEL_ID` from configuration?
4. Why is Converse easier to teach than a model-specific payload?
5. If the model ID is invalid, which layer is failing?

---

## Production gap

This example does not yet include:

- durable conversation history,
- retries/backoff,
- streaming,
- model fallback,
- token/cost controls,
- safety policies,
- application authentication.

Do not add all of them now. Each belongs to a later concept.

---

## Next day

Day 3 removes the focus from the model and teaches:

> What does a **Runtime session** preserve, and why is that still not durable Memory?

---

[Course index](../README.md) · [Teaching standard](../TEACHING_STANDARD.md)
