import os
from google.cloud import compute_v1


def find_stopped_instances(project_id: str):
    instances_client = compute_v1.InstancesClient()
    aggregated_list = instances_client.aggregated_list(project=project_id)

    findings = []

    for zone, response in aggregated_list:
        if response.instances:
            for instance in response.instances:
                if instance.status == "TERMINATED":
                    findings.append({
                        "name": instance.name,
                        "zone": zone,
                        "reason": "VM is stopped and may be stale",
                    })

    return findings


def run_stale_check():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        print("Please set GOOGLE_CLOUD_PROJECT first.")
        return

    print(f"\nChecking for stale resources in project: {project_id}\n")

    findings = find_stopped_instances(project_id)

    if not findings:
        print("No stale resources found.")
        return

    for finding in findings:
        print(f"- {finding['name']} | {finding['zone']} | {finding['reason']}")
