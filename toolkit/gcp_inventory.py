import os


def list_instances(project_id):
    from google.cloud import compute_v1
    client = compute_v1.InstancesClient()
    request = compute_v1.AggregatedListInstancesRequest(project=project_id)

    instances = []

    for zone, response in client.aggregated_list(request=request):
        if response.instances:
            for instance in response.instances:
                instances.append({
                    "name": instance.name,
                    "zone": zone,
                    "status": instance.status,
                })

    return instances


def list_buckets(project_id):
    from google.cloud import storage
    client = storage.Client(project=project_id)
    return [{"name": bucket.name} for bucket in client.list_buckets()]


def format_inventory_output(instances, buckets):
    lines = []

    lines.append("VM Instances:")
    if instances:
        for instance in instances:
            lines.append(f"  - {instance['name']} | {instance['zone']} | {instance['status']}")
    else:
        lines.append("  - No instances found")

    lines.append("")
    lines.append("Storage Buckets:")
    if buckets:
        for bucket in buckets:
            lines.append(f"  - {bucket['name']}")
    else:
        lines.append("  - No buckets found")

    return "\n".join(lines)


def run_inventory():
    from google.api_core.exceptions import Forbidden

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        print("Error: GOOGLE_CLOUD_PROJECT environment variable not set.")
        return

    print(f"\nInventory for project: {project_id}\n")

    instances = []
    buckets = []

    try:
        instances = list_instances(project_id)
    except Forbidden:
        print("Warning: insufficient permissions to list VM instances.\n")

    try:
        buckets = list_buckets(project_id)
    except Forbidden:
        print("Warning: insufficient permissions to list storage buckets.\n")

    print(format_inventory_output(instances, buckets))
    print()
