import json
import boto3
from botocore.exceptions import ClientError

REGION = "us-east-1"

def invoke_agent_via_boto3(agent_runtime_arn, message, runtime_client):
    """Invokes the Bedrock AgentCore Runtime directly using standard Boto3."""
    payload = {
        "input": {"text": message}
    }
    try:
        response = runtime_client.invoke_agent_runtime(
            agentRuntimeArn=agent_runtime_arn,
            payload=json.dumps(payload).encode("utf-8"),
            contentType="application/json"
        )

        if "response" in response:
            body = response["response"]
            data = body.read() if hasattr(body, "read") else body
            if isinstance(data, bytes):
                data = data.decode("utf-8")

            try:
                parsed = json.loads(data)
                for key in ["completion", "output", "result", "response", "text", "message"]:
                    if key in parsed:
                        return parsed[key]
                return parsed
            except json.JSONDecodeError:
                return data
        return None
    except ClientError as e:
        print(f"Boto3 Agent Invocation Error: {e}")
        return None


def main():
    # Initialize our three dedicated AWS service clients natively
    control_client = boto3.client("agent-registry-control", region_name=REGION)
    data_client    = boto3.client("agent-registry", region_name=REGION)
    runtime_client = boto3.client("bedrock-agentcore", region_name=REGION)

    # ------------------------------------------------------------------
    # 1. List and Select Registry (Control Plane)
    # ------------------------------------------------------------------
    print("\n=== Available Registries ===")
    try:
        list_resp = control_client.list_registries()
        registries = list_resp.get("registries", [])
        if not registries:
            print("No registries found.")
            return
        
        for idx, r in enumerate(registries, start=1):
            print(f"{idx}. {r.get('name')} (ID: {r.get('registryId')})")
            
        choice = int(input("\nSelect a registry by number: ")) - 1
        selected_registry = registries[choice]
        registry_id = selected_registry.get("registryId")
        
    except ClientError as e:
        print(f"API Error during registry listing: {e}")
        return

    # ------------------------------------------------------------------
    # 2. Native Data Plane Search (Boto3 Agent Registry Client)
    # ------------------------------------------------------------------
    search_query = input("\nEnter search query: ")
    print(f"\nSearching Registry '{registry_id}' for query '{search_query}'...")
    
    try:
        # Native Boto3 wrapper replacing the JSON-RPC "tools/call" pattern
        search_response = data_client.search_discoverable_registry_records(
            registryIds=[registry_id],
            searchQuery=search_query,
            maxResults=10
        )
        records = search_response.get("registryRecords", [])
        
    except ClientError as e:
        print(f"API Error during discovery search: {e}")
        return

    if not records:
        print("No matching records found.")
        return

    # ------------------------------------------------------------------
    # 3. Interactive Selection & Descriptor Parsing
    # ------------------------------------------------------------------
    print("\n=== Found Agents ===")
    agent_records = []
    for r in records:
        # Pull matching AGENT records that contain descriptor payloads
        if r.get("recordType") == "AGENT" and "descriptors" in r:
            agent_records.append(r)
            print(f"{len(agent_records)}. {r.get('name')} (ID: {r.get('recordId')})")

    if not agent_records:
        print("No agent records with an A2A Agent Card were found in the results.")
        return

    agent_choice = int(input("\nSelect an agent to invoke by number: ")) - 1
    target_agent = agent_records[agent_choice]

    # Native SDK returns 'descriptors' field layout as an object directly
    a2a_card = target_agent.get("descriptors", {}).get("a2aAgentCard", {})
    card_string = a2a_card.get("data", "{}")
    
    try:
        card_data = json.loads(card_string)
        agent_runtime_arn = card_data.get("url", "")
    except json.JSONDecodeError:
        print("Error: Could not decode A2A Agent Card JSON payload.")
        return

    if not agent_runtime_arn:
        print(f"Error: No operational runtime URL found inside the A2A card for {target_agent.get('name')}.")
        return

    # ------------------------------------------------------------------
    # 4. Direct Prompt Invocation (Bedrock Agent Runtime)
    # ------------------------------------------------------------------
    human_prompt = input("\nEnter prompt for the agent: ")

    print(f"\n=== Invoking Agent Core Runtime via Boto3: {target_agent.get('name')} ===")
    print(f"Target ARN: {agent_runtime_arn}")
    
    agent_response = invoke_agent_via_boto3(agent_runtime_arn, human_prompt, runtime_client)
    
    print("\n=== Agent Response ===")
    if isinstance(agent_response, (dict, list)):
        print(json.dumps(agent_response, indent=2))
    else:
        print(agent_response)


if __name__ == "__main__":
    main()
