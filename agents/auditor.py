def run(dossier):
    score = 0.0
    pillars = {}

    # Data continuity
    continuity = 0.0
    db = dossier.get("db", {})
    if db.get("pitr_enabled"):
        continuity += 0.3
    if db.get("backup_retention_days", 0) >= 7:
        continuity += 0.2
    if db.get("cross_region_replication") and db.get("cross_region_replication") != "none":
        continuity += 0.3
    pillars["data_continuity"] = round(continuity, 2)
    score += continuity * 30  # weight 30%

    # Failover
    infra = dossier.get("infra", {})
    failover = 0.0
    if db.get("multi_az"):
        failover += 0.2
    if infra.get("dns_failover"):
        failover += 0.3
    pillars["failover"] = round(failover, 2)
    score += failover * 25  # weight 25%

    # Other pillars (placeholder logic)
    pillars.setdefault("recovery_ops", 0.0)
    pillars.setdefault("security_integrity", 0.0)
    pillars.setdefault("observability", 0.0)

    return {"score": int(score), "pillars": pillars}
