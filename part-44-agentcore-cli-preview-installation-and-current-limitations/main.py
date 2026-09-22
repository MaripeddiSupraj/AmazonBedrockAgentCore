from bedrock_agentcore import BedrockAgentCoreApp

agent = BedrockAgentCoreApp()

@agent.handler()
def handler(input):
    text = input.get("text", "")
    return {
        "completion": f"Hello from your AgentCore container agent! You said: {text}",
        "stop_reason": "end_turn"
    }

if __name__ == "__main__":
    agent.run()
