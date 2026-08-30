import streamlit as st

from components.styles import inject_global_styles
from components.sidebar import render_sidebar_filters
from utils.data_loader import apply_filters, load_crm, load_reviews, load_sales
from utils.kpi_engine import run_full_analysis
from utils.security import apply_security_filter
from utils.telemetry import init_telemetry


def setup_page(title, icon="📊"):
  st.set_page_config(page_title=f"{title} | InsightFlow", page_icon=icon, layout="wide")
  inject_global_styles()
  init_telemetry()


def chart_layout(fig, height=300):
  fig.update_layout(
    height=height,
    margin=dict(l=0, r=0, t=8, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94A3B8"),
    xaxis=dict(showgrid=False, color="#64748B"),
    yaxis=dict(gridcolor="rgba(96,165,250,0.08)", color="#64748B"),
  )
  return fig


def load_context():
  sales_raw = load_sales()
  reviews_raw = load_reviews()
  crm_raw = load_crm()

  persona, date_range, region, product = render_sidebar_filters(sales_raw)
  filtered = apply_filters(sales_raw, date_range, region, product)

  if filtered.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

  sales, crm_display, access = apply_security_filter(filtered, crm_raw, persona)
  crm_for_analysis = crm_raw[crm_raw["region"].isin(access["regions"])].copy()
  analysis = run_full_analysis(sales, reviews_raw, crm_for_analysis)

  return {
    "persona": persona,
    "sales": sales,
    "crm": crm_display,
    "crm_raw": crm_for_analysis,
    "reviews": reviews_raw,
    "access": access,
    "analysis": analysis,
    "region": region,
    "product": product,
  }
