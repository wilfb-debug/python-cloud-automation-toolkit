import json
from pathlib import Path

SAMPLE_DATA_PATH = Path(__file__).parent.parent / "sample_data" / "billing_sample.json"


def load_cost_data(path=None):
    file_path = path or SAMPLE_DATA_PATH
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: billing data file not found at {file_path}")
        return None


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
            "alert": "Possible cost anomaly detected",
        }

    return {
        "today": today,
        "average": round(average, 2),
        "alert": "No anomaly detected",
    }


def run_cost_check():
    data = load_cost_data()
    if data is None:
        return

    result = detect_anomaly(data["daily_costs"])
    if result is None:
        print("Not enough data to check for anomalies.")
        return

    print("\nCost Check Result:\n")
    print(f"  Today's spend : ${result['today']}")
    print(f"  7-day average : ${result['average']}")
    print(f"  Status        : {result['alert']}")
    print()
