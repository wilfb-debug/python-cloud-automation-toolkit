import os


def find_stopped_instances(project_id):
    from google.cloud import compute_v1
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
                        "reason": "VM is stopped and may be stale",
                    })

    return findings


def format_stale_output(findings):
    lines = ["Stale Resource Findings:\n"]

    if findings:
        for finding in findings:
            lines.append(f"  - {finding['name']}")
            lines.append(f"    Zone   : {finding['zone']}")
            lines.append(f"    Reason : {finding['reason']}")
            lines.append("")
    else:
        lines.append("  - No stale resources found")

    return "\n".join(lines)


def run_stale_check():
    from google.api_core.exceptions import Forbidden

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        print("Error: GOOGLE_CLOUD_PROJECT environment variable not set.")
        return

    print(f"\nStale Resource Check for project: {project_id}\n")

    try:
        findings = find_stopped_instances(project_id)
    except Forbidden:
        print("Error: insufficient permissions to list VM instances.")
        return

    print(format_stale_output(findings))
