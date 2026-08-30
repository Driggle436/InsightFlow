import plotly.express as px
import streamlit as st

from ai.storyteller import generate_story
from components.action_cards import render_action_cards
from components.bento_layout import render_bento_shell
from components.confidence_panel import render_abstention_banner, render_confidence_gauge
from components.evidence_panel import render_driver_ranking
from components.html_render import render_html
from components.kpi_cards import render_alert_strip, render_kpi_grid
from components.layout import render_hero, render_section_header
from utils.bootstrap import chart_layout, load_context, setup_page

setup_page("Overview", "🏠")

try:
  ctx = load_context()
  persona = ctx["persona"]
  analysis = ctx["analysis"]

  render_bento_shell()
  render_hero(
    "Business Overview",
    f"What matters right now for {persona} — movements, drivers, and next steps.",
    badge="InsightFlow",
  )

  alerts = []
  if analysis["revenue_change"] < -3:
    alerts.append({
      "severity": "critical",
      "title": f"Revenue down {abs(analysis['revenue_change']):.1f}%",
      "detail": f"Biggest impact in {analysis['worst_region']} ({analysis['worst_change']:.1f}%)",
    })
  if analysis["negative_count"] >= 2:
    alerts.append({
      "severity": "warning",
      "title": f"{analysis['negative_count']} unhappy customers",
      "detail": "Delivery and service complaints in recent reviews",
    })
  if analysis["anomaly_count"] > 0:
    alerts.append({
      "severity": "info",
      "title": "Unusual revenue days",
      "detail": f"{analysis['anomaly_count']} days outside the normal pattern",
    })
  sparse_kpis = [k for k in analysis["kpis"] if k.get("sparse")]
  if sparse_kpis:
    alerts.append({
      "severity": "info",
      "title": "New product data is limited",
      "detail": f"{sparse_kpis[0]['name']} — only {sparse_kpis[0].get('history_days', '?')} days of history",
    })

  if alerts:
    render_alert_strip(alerts)

  render_section_header("Performance snapshot")
  render_kpi_grid(analysis["kpis"])

  chart_col, conf_col = st.columns([1.55, 1])

  with chart_col:
    render_section_header("Revenue trend")
    fig = px.area(
      analysis["daily_revenue"],
      x="date",
      y="revenue",
      color_discrete_sequence=["#60A5FA"],
    )
    chart_layout(fig)
    if analysis["anomaly_count"] > 0:
      fig.add_scatter(
        x=analysis["anomalies"]["date"],
        y=analysis["anomalies"]["revenue"],
        mode="markers",
        marker=dict(color="#F87171", size=9, symbol="circle"),
        name="Unusual",
      )
    st.plotly_chart(fig, use_container_width=True)

  with conf_col:
    render_section_header("How sure are we?")
    render_confidence_gauge(analysis["confidence_score"], analysis["confidence_components"])
    if analysis["confidence_score"] < 60:
      render_abstention_banner(
        "We're not confident enough to recommend strong action yet.",
        [
          "Confirm if a campaign or event affected the region",
          "Refresh customer data for the affected area",
          "Ask an analyst to validate before escalating",
        ],
      )

  left, right = st.columns(2)

  with left:
    render_section_header("What's driving the change")
    render_driver_ranking(analysis["drivers"][:3])

  with right:
    render_section_header("Recommended next steps")
    render_action_cards(analysis["recommendations"][:2], persona)

  render_section_header("Executive summary")

  if st.button("Generate insight narrative", type="primary"):
    with st.spinner("Preparing your summary..."):
      try:
        story = generate_story(
          persona=persona,
          revenue_change=analysis["revenue_change"],
          worst_region=analysis["worst_region"],
          worst_change=analysis["worst_change"],
          negative_reviews_count=analysis["negative_count"],
          regional_evidence=analysis["root_causes"],
          review_evidence=analysis["negative_reviews"],
        )
        st.session_state.generated_story = story
      except Exception:
        st.warning("Summary unavailable right now. Review the drivers and actions above.")

  if st.session_state.get("generated_story"):
    render_html(f'<div class="if-insight-card"><strong>For {persona}</strong></div>')
    st.markdown(st.session_state.generated_story)

except Exception as e:
  st.error(f"Unable to load overview: {e}")
