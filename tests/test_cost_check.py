from toolkit.cost_check import detect_anomaly


def test_detects_anomaly():
    daily_costs = [10, 12, 11, 10, 35]
    result = detect_anomaly(daily_costs)

    assert result["alert"] == "Possible cost anomaly detected"
    assert result["today"] == 35


def test_no_anomaly():
    daily_costs = [10, 12, 11, 10, 12]
    result = detect_anomaly(daily_costs)

    assert result["alert"] == "No anomaly detected"
    assert result["today"] == 12
