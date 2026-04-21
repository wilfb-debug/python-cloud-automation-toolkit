import os
from googleapiclient import discovery


RISKY_ROLES = {
    "roles/owner",
    "roles/editor",
}


def get_project_iam_policy(project_id: str):
    crm = discovery.build("cloudresourcemanager", "v1")
    request = crm.projects().getIamPolicy(
        resource=project_id,
        body={}
    )
    response = request.execute()
    return response


def find_risky_bindings(policy: dict):
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
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        print("Please set GOOGLE_CLOUD_PROJECT first.")
        return

    print(f"\nReviewing IAM for project: {project_id}\n")

    policy = get_project_iam_policy(project_id)
    findings = find_risky_bindings(policy)

    if not findings:
        print("No risky IAM bindings found.")
        return

    for finding in findings:
        print(
            f"- {finding['member']} has {finding['role']} "
            f"(risk: {finding['risk']})"
        )
