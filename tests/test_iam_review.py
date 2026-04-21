from toolkit.iam_review import find_risky_bindings


def test_find_risky_bindings_detects_owner_and_editor():
    policy = {
        "bindings": [
            {
                "role": "roles/owner",
                "members": ["user:test@example.com"]
            },
            {
                "role": "roles/editor",
                "members": ["serviceAccount:test@project.iam.gserviceaccount.com"]
            },
            {
                "role": "roles/viewer",
                "members": ["user:viewer@example.com"]
            }
        ]
    }

    findings = find_risky_bindings(policy)

    assert len(findings) == 2
    assert findings[0]["risk"] == "high"
    assert findings[1]["risk"] == "high"


def test_find_risky_bindings_returns_empty_for_safe_roles():
    policy = {
        "bindings": [
            {
                "role": "roles/viewer",
                "members": ["user:viewer@example.com"]
            }
        ]
    }

    findings = find_risky_bindings(policy)

    assert findings == []
