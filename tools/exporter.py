import json

def export(audit_result, sim_result, gaps, plan):
    with open("report.md", "w") as f:
        f.write("# DR Readiness Report\n")
        f.write("## Score\n")
        f.write(str(audit_result) + "\n")
        f.write("## Scenarios\n")
        f.write(str(sim_result) + "\n")
        f.write("## Gaps\n")
        f.write(str(gaps) + "\n")
        f.write("## Plan\n")
        f.write(str(plan) + "\n")

    with open("gaps.csv", "w") as f:
        f.write("scenario,achieved_rto,achieved_rpo,target_rto,target_rpo\n")
        for g in gaps:
            f.write(f"{g['scenario']},{g['achieved_rto']},{g['achieved_rpo']},{g['target_rto']},{g['target_rpo']}\n")
