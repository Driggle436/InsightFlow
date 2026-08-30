import streamlit as st

from components.html_render import render_html
from utils.display_labels import friendly_alert_detail


def _format_value(value, fmt):
  if fmt == "currency":
    return f"₹{value:,.0f}"
  if fmt == "percent":
    return f"{value:.1f}%"
  return f"{value:,.0f}"


def _delta_class(change):
  if change > 0.5:
    return "up"
  if change < -0.5:
    return "down"
  return "flat"


def _delta_text(change, fmt):
  if fmt == "percent":
    return f"{change:+.1f}pp" if change else "—"
  return f"{change:+.1f}%" if change else "—"


def render_kpi_grid(kpis):
  cards_html = ""
  for kpi in kpis:
    css_class = "if-kpi-card"
    if kpi.get("material"):
      css_class += " material"
    if kpi.get("sparse"):
      css_class += " sparse"

    badges = ""
    if kpi.get("material"):
      badges += '<span class="if-badge if-badge-p1" style="margin-left:6px">Needs attention</span>'
    if kpi.get("sparse"):
      days = kpi.get("history_days", "?")
      badges += f'<span class="if-badge if-badge-p3" style="margin-left:6px">New · {days}d</span>'

    meta = ""
    if kpi.get("sparse"):
      meta = '<div class="if-kpi-meta">Limited history — treat as directional only</div>'

    cards_html += (
      f'<div class="{css_class}">'
      f'<div class="if-kpi-label">{kpi["name"]}{badges}</div>'
      f'<div class="if-kpi-value">{_format_value(kpi["value"], kpi["format"])}</div>'
      f'<div class="if-kpi-delta {_delta_class(kpi["change"])}">{_delta_text(kpi["change"], kpi["format"])}</div>'
      f"{meta}</div>"
    )

  render_html(f'<div class="if-kpi-grid">{cards_html}</div>')


def render_alert_strip(alerts):
  items = ""
  for alert in alerts:
    detail = friendly_alert_detail(alert["detail"])
    items += (
      f'<div class="if-alert-item {alert["severity"]}">'
      f'<div class="if-alert-dot {alert["severity"]}"></div>'
      f"<div><strong>{alert['title']}</strong><br>"
      f'<span style="color:#64748B;font-size:0.82rem">{detail}</span></div>'
      f"</div>"
    )
  render_html(f'<div class="if-alert-strip">{items}</div>')
