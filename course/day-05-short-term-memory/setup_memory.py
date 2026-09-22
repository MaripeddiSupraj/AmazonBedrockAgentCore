import os

from bedrock_agentcore.memory import MemoryClient

REGION = os.getenv("AWS_REGION", "us-west-2")

client = MemoryClient(region_name=REGION)

memory = client.create_memory_and_wait(
    name="CourseDay05Memory",
    strategies=[],
    description="Short-term Memory resource for AgentCore course Day 5",
)

memory_id = memory.get("id") or memory.get("memoryId")

print("Memory is ACTIVE.")
print(f"MEMORY_ID={memory_id}")
print()
print("Export it before running the Day 5 agent:")
print(f'export MEMORY_ID="{memory_id}"')
