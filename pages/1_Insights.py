import plotly.express as px
import streamlit as st

from components.bento_layout import render_bento_shell
from components.confidence_panel import render_abstention_banner, render_confidence_gauge
from components.evidence_panel import render_driver_ranking, render_evidence_table
from components.kpi_cards import render_kpi_grid
from components.layout import render_hero, render_section_header
from utils.bootstrap import chart_layout, load_context, setup_page

setup_page("Insights", "💡")

try:
  ctx = load_context()
  analysis = ctx["analysis"]

  render_bento_shell()
  render_hero(
    "Insights",
    "Understand what changed, why it likely happened, and how reliable the explanation is.",
  )

  material = [k for k in analysis["kpis"] if k.get("material")]
  render_section_header("Movements that matter")
  if material:
    render_kpi_grid(material)
  else:
    st.success("No major KPI movements in this period.")

  col1, col2 = st.columns(2)

  with col1:
    render_section_header("Likely causes")
    render_driver_ranking(analysis["drivers"])

  with col2:
    render_section_header("Regional breakdown")
    if not analysis["root_causes"].empty:
      rc = analysis["root_causes"].reset_index()
      rc.columns = ["Region", "Previous", "Current", "Change", "Change %"]
      fig = px.bar(
        rc, x="Region", y="Change %",
        color="Change %",
        color_continuous_scale=["#F87171", "#FBBF24", "#34D399"],
        color_continuous_midpoint=0,
      )
      chart_layout(fig, height=340)
      fig.update_layout(showlegend=False)
      st.plotly_chart(fig, use_container_width=True)

  render_section_header("Trust in this insight")
  render_confidence_gauge(analysis["confidence_score"], analysis["confidence_components"])

  if analysis["confidence_score"] < 60:
    render_abstention_banner(
      "Evidence is mixed — we're holding back a firm recommendation.",
      [
        "Was there a promotion or supply issue in the affected region?",
        "Customer data may be stale — last CRM refresh was 3 days ago",
        "New products need more history before we act with confidence",
      ],
    )

  sparse_kpis = [k for k in analysis["kpis"] if k.get("sparse")]
  for kpi in sparse_kpis:
    st.info(
      f"**{kpi['name']}** only has {kpi.get('history_days', '?')} days of data. "
      "Treat trends as early signals, not conclusions."
    )

  render_section_header("Supporting evidence")
  render_evidence_table([
    {
      "source": "ERP / Sales DB",
      "method": "SQL",
      "detail": f"Revenue moved {analysis['revenue_change']:+.1f}% vs prior period",
      "freshness_label": "Today",
    },
    {
      "source": "CRM System",
      "method": "SQL",
      "detail": "Customer churn patterns align with regional decline",
      "freshness_label": "3 days ago",
    },
    {
      "source": "Review Platform API",
      "method": "ML",
      "detail": f"{analysis['negative_count']} negative reviews mention delivery issues",
      "freshness_label": "Recent",
    },
  ])

except Exception as e:
  st.error(f"Unable to load insights: {e}")
