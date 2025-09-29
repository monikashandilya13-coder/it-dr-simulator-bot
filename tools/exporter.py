import datetime
from pathlib import Path

def _badge(ok: bool) -> str:
    return "✅ Meets" if ok else "❌ Gap"

def _maturity(score: float) -> str:
    if score >= 0.8: return "Strong"
    if score >= 0.5: return "Moderate"
    if score > 0.0:  return "Weak"
    return "Missing"

def export_business_report(system_name: str, audit_result: dict, sim_result: dict, gaps: list, plan: dict, out_dir: str = ".") -> str:
    """Generate a business-friendly Markdown report and return its path."""
    out_path = Path(out_dir) / "DR_Readiness_Report.md"
    pillars = audit_result.get("pillars", {})
    overall_score = int(audit_result.get("score", 0))
    today = datetime.datetime.now().strftime("%d %b %Y")

    # Pillars expected keys (fill default 0 if missing)
    pkeys = ["data_continuity", "failover", "recovery_ops", "security_integrity", "observability"]
    for k in pkeys:
        pillars.setdefault(k, 0.0)

    def row_for_scenario(name, res, targets):
        rto = res.get("rto"); rpo = res.get("rpo"); meets = res.get("meets", False)
        trto = targets.get("rto_minutes", 0); trpo = targets.get("rpo_minutes", 0)
        risk = "Minimal disruption" if meets else ("Extended downtime, data loss" if name != "az_failure" else "Potential disruption")
        return f"| **{name.replace('_',' ').title()}** | {rto} min / {rpo} min | {trto} min / {trpo} min | {_badge(meets)} | {risk} |"

    targets = {
        "rto_minutes": gaps[0]["target_rto"] if gaps else 0,
        "rpo_minutes": gaps[0]["target_rpo"] if gaps else 0
    }

    md = []
    md.append("# 🏢 Disaster Recovery Readiness Assessment")
    md.append("")
    md.append(f"**System Assessed:** {system_name}")
    md.append(f"**Assessment Date:** {today}")
    md.append(f"**Assessor:** Automated DR Readiness Bot")
    md.append("")
    md.append("## 1. Executive Summary")
    md.append(f"- **Overall Readiness Score:** **{overall_score} / 100**" + (" (⚠️ Below Acceptable Threshold)" if overall_score < 60 else " (✅ Acceptable)"))
    md.append("- Current DR posture summary generated automatically from configuration and scenario simulations.")
    md.append("")
    md.append("## 2. DR Scorecard (by Pillar)")
    md.append("")
    md.append("| Pillar | Score (0–1) | Maturity | Remarks |")
    md.append("|---|---:|---|---|")
    md.append(f"| **Data Continuity** | {pillars['data_continuity']:.2f} | {_maturity(pillars['data_continuity'])} | Backups/PITR/replication |")
    md.append(f"| **Failover** | {pillars['failover']:.2f} | {_maturity(pillars['failover'])} | AZ/Region failover |")
    md.append(f"| **Recovery Ops** | {pillars['recovery_ops']:.2f} | {_maturity(pillars['recovery_ops'])} | Runbooks & drills |")
    md.append(f"| **Security & Integrity** | {pillars['security_integrity']:.2f} | {_maturity(pillars['security_integrity'])} | Keys, encryption, immutability |")
    md.append(f"| **Observability** | {pillars['observability']:.2f} | {_maturity(pillars['observability'])} | Alarms & backup monitoring |")
    md.append("")
    md.append("## 3. Scenario-Based Risk Assessment")
    md.append("")
    md.append("| Scenario | Achieved RTO / RPO | Target RTO / RPO | Status | Business Risk |")
    md.append("|---|---|---|---|---|")
    for sname, sres in sim_result.items():
        md.append(row_for_scenario(sname, sres, targets))
    md.append("")
    md.append("## 4. Key Gaps Identified")
    if gaps:
        for i, g in enumerate(gaps, 1):
            md.append(f"{i}. **{g['scenario'].replace('_',' ').title()}** – Achieved *{g['achieved_rto']}/{g['achieved_rpo']}* vs Target *{g['target_rto']}/{g['target_rpo']}* (RTO/RPO).")
    else:
        md.append("- No critical gaps detected.")
    md.append("")
    md.append("## 5. Recommended Remediation Plan (30/60/90 Days)")
    def list_block(title, items):
        md.append(f"- **{title}**")
        if items:
            for it in items:
                md.append(f"  - {it}")
        else:
            md.append("  - *(No items)*")
    list_block("30 Days – Quick Wins", plan.get("30_days", []))
    list_block("60 Days – Medium-Term Actions", plan.get("60_days", []))
    list_block("90 Days – Strategic Actions", plan.get("90_days", []))
    md.append("")
    md.append("## 6. Business Prioritization Matrix (auto)")
    md.append("")
    md.append("| Gap / Scenario | Likelihood | Impact | Priority |")
    md.append("|---|---|---|---|")
    # Naive matrix based on scenario type
    for g in gaps:
        scen = g['scenario']
        if scen == "region_failure":
            like, imp, pri = "High", "Critical", "🔴 Top"
        elif scen == "logical_corruption":
            like, imp, pri = "Medium", "Critical", "🔴 Top"
        else:
            like, imp, pri = "Medium", "High", "🟠 High"
        md.append(f"| {scen.replace('_',' ').title()} | {like} | {imp} | {pri} |")
    md.append("")
    md.append("## 7. Overall Recommendation")
    md.append("Prioritize regional resilience (cross-region replication & DNS failover) and data integrity (PITR + tested restores). Establish monitoring and runbooks, then run a full DR drill.")
    out_path.write_text("\n".join(md), encoding="utf-8")
    return str(out_path)

def export_raw(audit_result, sim_result, gaps, plan, out_dir: str = ".") -> str:
    """Legacy raw export; kept for reference."""
    out_path = Path(out_dir) / "report.md"
    with open(out_path, "w") as f:
        f.write("# DR Readiness Report\n")
        f.write("## Score\n")
        f.write(str(audit_result) + "\n")
        f.write("## Scenarios\n")
        f.write(str(sim_result) + "\n")
        f.write("## Gaps\n")
        f.write(str(gaps) + "\n")
        f.write("## Plan\n")
        f.write(str(plan) + "\n")
    return str(out_path)
