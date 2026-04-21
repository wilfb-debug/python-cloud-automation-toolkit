from toolkit.stale_check import format_stale_output


def test_stale_output_with_findings():
    findings = [
        {
            "name": "old-vm",
            "zone": "zones/europe-west2-a",
            "reason": "VM is stopped and may be stale"
        }
    ]

    result = format_stale_output(findings)

    assert "Stale Resource Findings:" in result
    assert "- old-vm | zones/europe-west2-a | VM is stopped and may be stale" in result


def test_stale_output_empty():
    result = format_stale_output([])

    assert "Stale Resource Findings:" in result
    assert "- No stale resources found" in result
