permit (
    principal,
    action == AgentCore::Action::"myWeatherTool___myWeatherTool",
    resource ==
        AgentCore::Gateway::"arn:aws:bedrock-agentcore:us-east-1:123456789012:gateway/mynewgateway-bfk3p2xlqx"
)
when { (context.input).city == "Chicago" };