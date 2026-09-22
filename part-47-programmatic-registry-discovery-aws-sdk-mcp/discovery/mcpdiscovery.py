import itertools
import json
import boto3
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

REGION = "us-east-1"
SERVICE = "agent-registry"
MCP_PROTOCOL_VERSION = "2025-11-25"
_ids = itertools.count(1)


def mcp_call(endpoint, region, creds, registry_id, method, params=None):
    url = f"{endpoint}/registry/{registry_id}/mcp"
    payload = {"jsonrpc": "2.0", "method": method}

    if not method.startswith("notifications/"):
        payload["id"] = next(_ids)
    if params is not None:
        payload["params"] = params

    body = json.dumps(payload).encode()
    signed = AWSRequest(method="POST", url=url, data=body,
                        headers={"Content-Type": "application/json"})
    SigV4Auth(creds, SERVICE, region).add_auth(signed)

    resp = requests.post(url, data=body, headers=dict(signed.headers), timeout=30)
    resp.raise_for_status()
    return resp.json() if resp.content else None


def tool_payload(result):
    content = (result or {}).get("content") or []
    if not content:
        return None
    text = content[0].get("text", "")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def main():
    session = boto3.Session()
    creds = session.get_credentials().get_frozen_credentials()

    # Control plane for management operations
    control_client = boto3.client("agent-registry-control", region_name=REGION)

    # -----------------------------------------------------------------------
    # 1. List registries dynamically
    # -----------------------------------------------------------------------
    print("\n=== Available Registries ===")
    registries = control_client.list_registries()

    if not registries["registries"]:
        raise RuntimeError("No registries found.")

    for idx, r in enumerate(registries["registries"], start=1):
        print(f"{idx}. {r['name']}  ({r['registryArn']})")

    # -----------------------------------------------------------------------
    # 2. User selects registry
    # -----------------------------------------------------------------------
    choice = int(input("\nSelect a registry by number: "))
    selected = registries["registries"][choice - 1]

    registry_name = selected["name"]
    registry_arn  = selected["registryArn"]
    registry_id   = registry_arn.split("/")[-1]

    print(f"\nUsing registry: {registry_name}")
    print(f"Registry ID:    {registry_id}")

    endpoint = f"https://agent-registry.{REGION}.api.aws"

    # -----------------------------------------------------------------------
    # 3. MCP initialize
    # -----------------------------------------------------------------------
    print("\n=== MCP initialize ===")
    init = mcp_call(endpoint, REGION, creds, registry_id, "initialize", {
        "protocolVersion": MCP_PROTOCOL_VERSION,
        "capabilities": {},
        "clientInfo": {"name": "demo-client", "version": "1.0"},
    })
    print(json.dumps(init, indent=2))

    mcp_call(endpoint, REGION, creds, registry_id, "notifications/initialized")

    # -----------------------------------------------------------------------
    # 4. MCP tools/list
    # -----------------------------------------------------------------------
    print("\n=== MCP tools/list ===")
    listed = mcp_call(endpoint, REGION, creds, registry_id, "tools/list", {})
    print(json.dumps(listed, indent=2))

    # -----------------------------------------------------------------------
    # 5. User enters search query
    # -----------------------------------------------------------------------
    search_query = input("\nEnter search query: ")

    # -----------------------------------------------------------------------
    # 6. MCP tools/call search_discoverable_registry_records
    # -----------------------------------------------------------------------
    print("\n=== MCP search_discoverable_registry_records ===")
    called = mcp_call(endpoint, REGION, creds, registry_id, "tools/call", {
        "name": "search_discoverable_registry_records",
        "arguments": {
            "searchQuery": search_query,
            "maxResults": 10,
            "filter": {"recordType": {"$eq": "MCP"}},
        },
    })

    if "error" in called:
        print("JSON-RPC error:")
        print(json.dumps(called["error"], indent=2))
        return

    result = called.get("result", {})
    if result.get("isError"):
        print("Tool error:")
        print(tool_payload(result))
        return

    records = tool_payload(result)
    print(json.dumps(records, indent=2))

    print("\nDone.")


if __name__ == "__main__":
    main()
