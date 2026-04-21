import os
from google.cloud import compute_v1
from google.api_core.exceptions import Forbidden


def find_stopped_instances(project_id):
    client = compute_v1.InstancesClient()
    request = compute_v1.AggregatedListInstancesRequest(project=project_id)

    findings = []

    for zone, response in client.aggregated_list(request=request):
        if response.instances:
            for instance in response.instances:
                if instance.status == "TERMINATED":
                    findings.append({
                        "name": instance.name,
                        "zone": zone,
                        "reason": "VM is stopped and may be stale"
                    })

    return findings


def format_stale_output(findings):
    lines = ["Stale Resource Findings:"]

    if findings:
        for finding in findings:
            lines.append(
                f"- {finding['name']} | {finding['zone']} | {finding['reason']}"
            )
    else:
        lines.append("- No stale resources found")

    return "\n".join(lines)


def run_stale_check():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        print("Please set GOOGLE_CLOUD_PROJECT first.")
        return

    print(f"\nChecking stale resources for project: {project_id}\n")

    try:
        findings = find_stopped_instances(project_id)
    except Forbidden as error:
        print(f"Could not check stale resources: {error}")
        return

    print(format_stale_output(findings))
