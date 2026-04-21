import json
from pathlib import Path


def load_cost_data():
    file_path = Path("sample_data/billing_sample.json")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def detect_anomaly(daily_costs):
    if len(daily_costs) < 2:
        return None

    today = daily_costs[-1]
    previous_days = daily_costs[:-1]
    average = sum(previous_days) / len(previous_days)

    if today > average * 1.5:
        return {
            "today": today,
            "average": round(average, 2),
            "alert": "Possible cost anomaly detected"
        }

    return {
        "today": today,
        "average": round(average, 2),
        "alert": "No anomaly detected"
    }


def run_cost_check():
    data = load_cost_data()
    result = detect_anomaly(data["daily_costs"])

    print("\nCost Check Result:\n")
    print(f"Today: {result['today']}")
    print(f"Average: {result['average']}")
    print(f"Status: {result['alert']}")
