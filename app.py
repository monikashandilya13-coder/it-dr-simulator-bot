import streamlit as st
import json
from agents import auditor, simulator, critic, planner
from tools import exporter

st.title("Disaster Recovery Readiness Bot")

uploaded_file = st.file_uploader("Upload System Dossier JSON", type="json")
if uploaded_file:
    dossier = json.load(uploaded_file)

    # Run agents
    audit_result = auditor.run(dossier)
    sim_result = simulator.run(dossier, audit_result)
    gaps = critic.run(sim_result, dossier)
    plan = planner.run(gaps)

    st.subheader("Overall DR Score")
    st.progress(audit_result["score"]/100)
    st.json(audit_result["pillars"])

    st.subheader("Scenario Results")
    st.json(sim_result)

    st.subheader("Identified Gaps")
    st.json(gaps)

    st.subheader("30/60/90 Remediation Plan")
    st.json(plan)

    if st.button("Export Report"):
        exporter.export(audit_result, sim_result, gaps, plan)
        st.success("Exported to report.md and gaps.csv")
