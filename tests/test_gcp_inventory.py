from toolkit.gcp_inventory import format_inventory_output


def test_format_inventory_with_resources():
    instances = [
        {
            "name": "test-vm",
            "zone": "zones/europe-west2-a",
            "status": "RUNNING"
        }
    ]
    buckets = [
        {"name": "test-bucket"}
    ]

    result = format_inventory_output(instances, buckets)

    assert "VM Instances:" in result
    assert "- test-vm | zones/europe-west2-a | RUNNING" in result
    assert "Storage Buckets:" in result
    assert "- test-bucket" in result


def test_format_inventory_with_no_resources():
    result = format_inventory_output([], [])

    assert "VM Instances:" in result
    assert "- No instances found" in result
    assert "Storage Buckets:" in result
    assert "- No buckets found" in result
