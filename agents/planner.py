def run(gaps):
    plan = {"30_days": [], "60_days": [], "90_days": []}
    # Quick baseline actions always useful
    quick_wins = [
        "Create DR runbook (roles, steps, cutover criteria).",
        "Configure alarms for backup failures and replication lag."
    ]
    for q in quick_wins:
        if q not in plan["30_days"]:
            plan["30_days"].append(q)

    for g in gaps:
        scen = g.get("scenario")
        if scen == "az_failure":
            if "Enable Multi-AZ failover with automated monitoring." not in plan["60_days"]:
                plan["60_days"].append("Enable Multi-AZ failover with automated monitoring.")
        elif scen == "region_failure":
            if "Set up cross-region database replication." not in plan["60_days"]:
                plan["60_days"].append("Set up cross-region database replication.")
            if "Configure DNS failover for automated redirection." not in plan["60_days"]:
                plan["60_days"].append("Configure DNS failover for automated redirection.")
        elif scen == "logical_corruption":
            if "Enable Point-In-Time Recovery (PITR) and test restores." not in plan["90_days"]:
                plan["90_days"].append("Enable Point-In-Time Recovery (PITR) and test restores.")
            if "Conduct a full DR drill including corruption scenario." not in plan["90_days"]:
                plan["90_days"].append("Conduct a full DR drill including corruption scenario.")
    return plan
