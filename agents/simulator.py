def run(dossier, audit_result):
    targets = dossier.get("targets", {})
    rto = targets.get("rto_minutes", 30)
    rpo = targets.get("rpo_minutes", 15)

    scenarios = {
        "az_failure": {"rto": 5 if dossier["db"].get("multi_az") else 60, "rpo": 0},
        "region_failure": {"rto": 120, "rpo": 60},
        "logical_corruption": {"rto": 90, "rpo": 30}
    }

    for s in scenarios:
        scenarios[s]["meets"] = scenarios[s]["rto"] <= rto and scenarios[s]["rpo"] <= rpo

    return scenarios
