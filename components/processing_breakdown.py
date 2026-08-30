import streamlit as st

from components.html_render import render_html


def render_processing_pipeline(steps):
  pipeline_html = ""
  for step in steps:
    css = "if-pipeline-step"
    if step.get("method") == "llm":
      css += " llm"
    elif step.get("active"):
      css += " active"

    icon = {"sql": "SQL", "ml": "ML", "stats": "STAT", "rules": "RULE", "llm": "LLM"}.get(
      step.get("method", "sql"), "DATA"
    )

    pipeline_html += (
      f'<div class="{css}">'
      f'<div class="if-pipeline-icon">{icon}</div>'
      f'<div class="if-pipeline-label">{step["step"]}</div>'
      f'<div class="if-pipeline-type">{step.get("method", "").upper()} · {step.get("duration_ms", 0)}ms</div>'
      f"</div>"
    )

  render_html(f'<div class="if-pipeline">{pipeline_html}</div>')


def render_llm_vs_deterministic():
  col1, col2 = st.columns(2)
  with col1:
    st.markdown(
      """
      **Deterministic Processing (Source of Truth)**
      - SQL aggregations for KPI values
      - IsolationForest anomaly detection
      - Period-over-period contribution analysis
      - TextBlob sentiment scoring
      - Weighted confidence scoring (business rules)
      - P1–P3 action prioritization (rule engine)
      """,
    )
  with col2:
    st.markdown(
      """
      **LLM Processing (Narrative Only)**
      - Persona-specific insight narrative synthesis
      - Evidence citation in plain language
      - Abstention when evidence is insufficient
      - **Never** computes KPIs or driver rankings
      - Token usage tracked per call
      """,
    )
