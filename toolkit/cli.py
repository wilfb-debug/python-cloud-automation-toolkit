import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Python Cloud Automation Toolkit"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("inventory", help="List GCP resources")
    subparsers.add_parser("iam-review", help="Review IAM access")
    subparsers.add_parser("stale-check", help="Find stale resources")
    subparsers.add_parser("cost-check", help="Check for cost anomalies")

    args = parser.parse_args()

    if args.command == "inventory":
        from toolkit.gcp_inventory import run_inventory
        run_inventory()
    elif args.command == "iam-review":
        from toolkit.iam_review import run_iam_review
        run_iam_review()
    elif args.command == "stale-check":
        from toolkit.stale_check import run_stale_check
        run_stale_check()
    elif args.command == "cost-check":
        from toolkit.cost_check import run_cost_check
        run_cost_check()


if __name__ == "__main__":
    main()
