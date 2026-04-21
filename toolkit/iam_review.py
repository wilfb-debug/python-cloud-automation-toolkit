import os


RISKY_ROLES = {
    "roles/owner",
    "roles/editor",
}


def get_project_iam_policy(project_id):
    from googleapiclient import discovery
    crm = discovery.build("cloudresourcemanager", "v1")
    request = crm.projects().getIamPolicy(resource=project_id, body={})
    return request.execute()


def find_risky_bindings(policy):
    findings = []

    for binding in policy.get("bindings", []):
        role = binding.get("role")
        members = binding.get("members", [])

        if role in RISKY_ROLES:
            for member in members:
                findings.append({
                    "role": role,
                    "member": member,
                    "risk": "high",
                })

    return findings


def run_iam_review():
    from googleapiclient.errors import HttpError

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        print("Error: GOOGLE_CLOUD_PROJECT environment variable not set.")
        return

    print(f"\nIAM Review for project: {project_id}\n")

    try:
        policy = get_project_iam_policy(project_id)
    except HttpError as e:
        print(f"Error: could not retrieve IAM policy — {e}")
        return

    findings = find_risky_bindings(policy)

    if not findings:
        print("No risky IAM bindings found.")
        print()
        return

    print(f"Found {len(findings)} risky binding(s):\n")
    for finding in findings:
        print(f"  - {finding['member']}")
        print(f"    Role : {finding['role']}")
        print(f"    Risk : {finding['risk']}")
        print()
