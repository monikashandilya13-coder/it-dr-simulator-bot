def run(dossier):
    score = 0
    pillars = {}

    # Data continuity
    continuity = 0
    if dossier["db"].get("pitr_enabled"):
        continuity += 0.3
    if dossier["db"].get("backup_retention_days", 0) >= 7:
        continuity += 0.2
    if dossier["db"].get("cross_region_replication") != "none":
        continuity += 0.3
    pillars["data_continuity"] = round(continuity, 2)
    score += continuity * 30

    # Failover
    failover = 0.2 if dossier["db"].get("multi_az") else 0
    if dossier.get("infra", {}).get("dns_failover"):
        failover += 0.3
    pillars["failover"] = round(failover, 2)
    score += failover * 25

    return {
        "score": int(score),
        "pillars": pillars
    }
