def run(sim_result, dossier):
    targets = dossier.get("targets", {})
    rto = targets.get("rto_minutes", 30)
    rpo = targets.get("rpo_minutes", 15)

    gaps = []
    for scenario, res in sim_result.items():
        if not res["meets"]:
            gaps.append({
                "scenario": scenario,
                "achieved_rto": res["rto"],
                "achieved_rpo": res["rpo"],
                "target_rto": rto,
                "target_rpo": rpo
            })
    return gaps
