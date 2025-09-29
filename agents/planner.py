def run(gaps):
    plan = {"30_days": [], "60_days": [], "90_days": []}

    for g in gaps:
        if g["scenario"] == "az_failure":
            plan["30_days"].append("Enable Multi-AZ failover with automated monitoring.")
        elif g["scenario"] == "region_failure":
            plan["60_days"].append("Establish cross-region replica and Route53 failover.")
        elif g["scenario"] == "logical_corruption":
            plan["90_days"].append("Enable PITR and test restore from backups.")

    return plan
