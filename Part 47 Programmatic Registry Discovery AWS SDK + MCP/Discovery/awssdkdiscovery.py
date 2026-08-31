import boto3
from botocore.exceptions import ClientError

REGION = "us-east-1"

# ✅ Two separate clients - control plane and data plane
control_client = boto3.client("agent-registry-control", region_name=REGION)
data_client    = boto3.client("agent-registry", region_name=REGION)

# ------------------------------------------------------------------
# 1. List all registries (control plane)
# ------------------------------------------------------------------
print("=== Available Registries ===")
try:
    response = control_client.list_registries()
    registries = response.get("registries", [])
    if not registries:
        print("No registries found.")
    for registry in registries:
        print(f"  - {registry.get('registryId')} | {registry.get('name')} | Status: {registry.get('status')}")
except ClientError as e:
    print(f"API Error during registry listing: {e}")

# ------------------------------------------------------------------
# 2. List registry records (control plane)
# ------------------------------------------------------------------
print("\n=== Registry Records ===")
try:
    response = control_client.list_registries()
    registries = response.get("registries", [])
    for registry in registries:
        registry_id = registry.get("registryId")
        print(f"\nRegistry: {registry_id}")
        try:
            records_response = control_client.list_registry_records(
                registryId=registry_id
            )
            records = records_response.get("registryRecords", [])
            if not records:
                print("  No records found.")
            for record in records:
                print(f"  - {record.get('recordId')} | {record.get('name')} | Status: {record.get('status')}")
        except ClientError as e:
            print(f"  Error listing records for {registry_id}: {e}")
except ClientError as e:
    print(f"API Error: {e}")

# ------------------------------------------------------------------
# 3. List discoverable (approved) registry records (data plane)
# ------------------------------------------------------------------
print("\n=== Discoverable Registry Records ===")
try:
    response = control_client.list_registries()
    registries = response.get("registries", [])
    for registry in registries:
        registry_id = registry.get("registryId")
        print(f"\nRegistry: {registry_id}")
        try:
            discoverable_response = data_client.list_discoverable_registry_records(
                registryId=registry_id
            )
            records = discoverable_response.get("registryRecords", [])
            if not records:
                print("  No approved/discoverable records found.")
            for record in records:
                print(f"  - {record.get('recordId')} | {record.get('name')} | Type: {record.get('recordType')}")
        except ClientError as e:
            print(f"  Error listing discoverable records for {registry_id}: {e}")
except ClientError as e:
    print(f"API Error: {e}")

# ------------------------------------------------------------------
# 4. Search discoverable registry records (data plane)
# ------------------------------------------------------------------
print("\n=== Search Discoverable Registry Records ===")
try:
    response = control_client.list_registries()
    registries = response.get("registries", [])
    for registry in registries:
        registry_id = registry.get("registryId")
        print(f"\nRegistry: {registry_id}")
        try:
            search_response = data_client.search_discoverable_registry_records(
                registryIds=[registry_id],
                searchQuery="agent",
                maxResults=10
            )
            results = search_response.get("registryRecords", [])
            if not results:
                print("  No search results found.")
            for result in results:
                print(f"  - {result.get('recordId')} | {result.get('name')}")
        except ClientError as e:
            print(f"  Error searching records for {registry_id}: {e}")
except ClientError as e:
    print(f"API Error: {e}")
