import os

import boto3
from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

REGION = os.getenv("AWS_REGION", "us-west-2")
MODEL_ID = os.getenv("MODEL_ID", "")
bedrock = boto3.client("bedrock-runtime", region_name=REGION)


@app.entrypoint
def handler(request):
    """Day 2: AgentCore Runtime hosts the app; Bedrock performs inference."""
    prompt = request.get("prompt")

    if not isinstance(prompt, str) or not prompt.strip():
        return {"ok": False, "message": "Send a non-empty 'prompt' string."}

    if not MODEL_ID:
        return {
            "ok": False,
            "message": "MODEL_ID is not configured.",
        }

    response = bedrock.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt.strip()}],
            }
        ],
        inferenceConfig={
            "maxTokens": 300,
            "temperature": 0.2,
        },
    )

    blocks = response["output"]["message"]["content"]
    text = "".join(block.get("text", "") for block in blocks if "text" in block)

    return {
        "ok": True,
        "message": text,
        "model_id": MODEL_ID,
        "hosted_by": "agentcore-runtime",
        "inference_by": "bedrock-runtime",
    }


if __name__ == "__main__":
    app.run()
