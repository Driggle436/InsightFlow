import pandas as pd
import streamlit as st

from components.html_render import render_html
from components.processing_breakdown import render_llm_vs_deterministic, render_processing_pipeline
from components.telemetry_panel import render_telemetry_dashboard
from utils.semantic_contract import DATA_SOURCES, KPI_CONTRACTS
from utils.telemetry import get_telemetry_summary


def render_engine_room(ctx):
  persona = ctx["persona"]
  access = ctx["access"]
  analysis = ctx["analysis"]

  st.caption("Technical view — methods, lineage, telemetry, and contracts (not shown to business users).")

  tab_telemetry, tab_lineage, tab_contracts, tab_architecture = st.tabs(
    ["Telemetry", "Data Lineage", "KPI Contracts", "Processing Architecture"]
  )

  with tab_telemetry:
    render_telemetry_dashboard()
    summary = get_telemetry_summary()
    if summary["pipeline_steps"]:
      st.markdown("#### Pipeline timings")
      render_processing_pipeline(summary["pipeline_steps"])

  with tab_lineage:
    lineage_steps = [
      ("sales_transactions", "SQL", "Raw transaction data loaded from ERP"),
      ("daily_revenue", "SQL Aggregation", f"Daily rollup → {len(analysis['daily_revenue'])} points"),
      ("anomaly_detection", "IsolationForest", f"{analysis['anomaly_count']} anomalies flagged"),
      ("regional_contribution", "Period Comparison", f"Worst: {analysis['worst_region']} ({analysis['worst_change']:+.1f}%)"),
      ("crm_reconciliation", "SQL Join", "Churn merged with regional revenue"),
      ("sentiment_analysis", "TextBlob ML", f"{analysis['negative_count']} negative reviews"),
      ("confidence_scoring", "Business Rules", f"Score: {analysis['confidence_score']}%"),
      ("narrative_synthesis", "LLM (Gemini)", "Persona narrative"),
    ]
    for i, (step, method, detail) in enumerate(lineage_steps, 1):
      render_html(
        f'<div class="if-evidence-row" style="background:rgba(255,255,255,0.7);border-radius:8px;margin-bottom:6px;padding:12px 16px">'
        f"<span style='font-weight:600;color:#1E40AF;min-width:24px'>{i}.</span>"
        f"<span class='if-evidence-source' style='min-width:160px'>{step}</span>"
        f"<span class='if-evidence-detail'><code>{method}</code> — {detail}</span></div>"
      )

    st.markdown("#### Data sources")
    for source in DATA_SOURCES:
      render_html(
        f'<div class="if-contract-card"><div class="if-contract-name">{source["name"]}</div>'
        f'<div class="if-contract-detail">Table: <code>{source["table"]}</code> | '
        f'Grain: {source["grain"]} | Refresh: {source["refresh"]} | '
        f'Quality: {source["quality_score"]}/100</div></div>'
      )

    st.markdown("#### Security entitlements")
    st.json({
      "persona": persona,
      "regions": access["regions"],
      "columns": access["columns"],
      "crm_detail": access["can_see_crm_detail"],
      "customer_pii": access["can_see_customer_pii"],
    })

  with tab_contracts:
    for contract in KPI_CONTRACTS:
      access_level = contract["access"].get(persona, "none")
      render_html(
        f'<div class="if-contract-card"><div class="if-contract-name">{contract["name"]} '
        f'<span class="if-badge if-badge-secure">{access_level}</span></div>'
        f'<div class="if-contract-detail"><code>{contract["formula"]}</code><br>'
        f'Lineage: {" → ".join(contract["lineage"])}</div></div>'
      )

  with tab_architecture:
    render_llm_vs_deterministic()
    st.markdown(
      """
      | Step | Method | Source of truth |
      |------|--------|----------------|
      | KPI values | SQL | Yes |
      | Anomalies | IsolationForest | Yes |
      | Root cause | Period comparison | Yes |
      | Sentiment | TextBlob | Yes |
      | Confidence | Business rules | Yes |
      | Narrative | Gemini Flash Lite | No |
      """
    )
