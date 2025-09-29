import streamlit as st
import json
from agents import auditor, simulator, critic, planner
from tools import exporter
from pathlib import Path

st.set_page_config(page_title="DR Readiness Bot", layout="wide")
st.title("🏢 Disaster Recovery Readiness Bot")

uploaded_file = st.file_uploader("Upload System Dossier JSON", type="json")
system_name = st.text_input("System Name (for the report)", value="Payroll-System")

if uploaded_file:
    dossier = json.load(uploaded_file)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎯 Targets")
        st.json(dossier.get("targets", {}))

    # Run agents
    audit_result = auditor.run(dossier)
    sim_result = simulator.run(dossier, audit_result)
    gaps = critic.run(sim_result, dossier)
    plan = planner.run(gaps)

    st.markdown("### 📊 Overall DR Score")
    st.metric("Score", f"{audit_result['score']} / 100")
    st.progress(audit_result["score"]/100)

    st.markdown("### 🧱 Pillar Scores")
    st.json(audit_result["pillars"])

    st.markdown("### 🔎 Scenario Results")
    st.json(sim_result)

    st.markdown("### ⚠️ Identified Gaps")
    st.json(gaps)

    st.markdown("### 🛠️ 30/60/90 Remediation Plan")
    st.json(plan)

    if st.button("📄 Generate Business Report"):
        out_path = exporter.export_business_report(system_name, audit_result, sim_result, gaps, plan, out_dir=".")
        st.success(f"Report generated: {out_path}")
        # Provide a download link
        with open(out_path, "rb") as f:
            st.download_button("Download DR_Readiness_Report.md", f, file_name="DR_Readiness_Report.md", mime="text/markdown")
