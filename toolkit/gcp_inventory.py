import os
from google.cloud import compute_v1
from google.cloud import storage
from google.api_core.exceptions import Forbidden


def list_instances(project_id):
    client = compute_v1.InstancesClient()
    request = compute_v1.AggregatedListInstancesRequest(project=project_id)

    instances = []

    for zone, response in client.aggregated_list(request=request):
        if response.instances:
            for instance in response.instances:
                instances.append({
                    "name": instance.name,
                    "zone": zone,
                    "status": instance.status
                })

    return instances


def list_buckets(project_id):
    client = storage.Client(project=project_id)
    buckets = client.list_buckets()

    return [{"name": bucket.name} for bucket in buckets]


def format_inventory_output(instances, buckets):
    lines = []

    lines.append("VM Instances:")
    if instances:
        for instance in instances:
            lines.append(f"- {instance['name']} | {instance['zone']} | {instance['status']}")
    else:
        lines.append("- No instances found")

    lines.append("")
    lines.append("Storage Buckets:")
    if buckets:
        for bucket in buckets:
            lines.append(f"- {bucket['name']}")
    else:
        lines.append("- No buckets found")

    return "\n".join(lines)


def run_inventory():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        print("Please set GOOGLE_CLOUD_PROJECT")
        return

    print(f"\nInventory for project: {project_id}\n")

    try:
        instances = list_instances(project_id)
    except Forbidden as error:
        print(f"VM Instances:\n- Could not list instances: {error}")
        instances = []

    try:
        buckets = list_buckets(project_id)
    except Forbidden as error:
        print(f"\nStorage Buckets:\n- Could not list buckets: {error}")
        buckets = []

    print(format_inventory_output(instances, buckets))
