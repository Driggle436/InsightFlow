import streamlit as st
import plotly.graph_objects as go

from components.html_render import render_html


def render_confidence_gauge(score, components):
  color = "#34D399" if score >= 80 else "#FBBF24" if score >= 60 else "#F87171"
  label = "High" if score >= 80 else "Medium" if score >= 60 else "Low"

  fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=score,
    number={"suffix": "%", "font": {"size": 28, "family": "Fira Code", "color": "#E2E8F0"}},
    gauge={
      "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#64748B"},
      "bar": {"color": color, "thickness": 0.7},
      "bgcolor": "rgba(15,23,42,0.8)",
      "borderwidth": 0,
      "steps": [
        {"range": [0, 60], "color": "rgba(248,113,113,0.25)"},
        {"range": [60, 80], "color": "rgba(251,191,36,0.25)"},
        {"range": [80, 100], "color": "rgba(52,211,153,0.25)"},
      ],
    },
    title={"text": f"Confidence: {label}", "font": {"size": 14, "color": "#94A3B8"}},
  ))
  fig.update_layout(
    height=220,
    margin=dict(l=20, r=20, t=40, b=10),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#E2E8F0"),
  )

  col1, col2 = st.columns([1, 2])
  with col1:
    st.plotly_chart(fig, use_container_width=True)
  with col2:
    labels = {
      "Data Freshness": "How current the data is",
      "Data Completeness": "How complete the data is",
      "Statistical Strength": "How strong the signal is",
      "Evidence Quality": "How well sources agree",
    }
    for factor, value in components.items():
      st.progress(value / 100, text=f"{labels.get(factor, factor)}: {value}%")


def render_abstention_banner(reason, suggestions):
  suggestions_html = "".join(f"<li>{s}</li>" for s in suggestions)
  render_html(
    f'<div class="if-abstain-banner">'
    f"<h3>Not enough evidence yet</h3>"
    f"<p>{reason}</p>"
    f'<ul style="margin:8px 0 0 0;padding-left:20px;font-size:0.85rem">'
    f"{suggestions_html}</ul></div>"
  )
