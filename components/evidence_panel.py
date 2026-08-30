import streamlit as st

from components.html_render import render_html
from utils.display_labels import friendly_source


def render_driver_ranking(drivers, show_technical=False):
  if not drivers:
    st.info("No significant drivers detected for the current period.")
    return

  for i, driver in enumerate(drivers, 1):
    conf_class = f"if-badge-{driver['confidence'].lower()}"
    method_badge = ""
    if show_technical:
      method_badge = f'<span class="if-badge if-badge-stats">{driver["method"]}</span>'

    render_html(
      f'<div class="if-action-card">'
      f'<div class="if-action-header">'
      f'<span style="font-weight:800;color:#1E40AF;font-size:1.1rem">#{i}</span>'
      f'<span class="if-action-title">{driver["driver"]}</span>'
      f'<span class="if-badge {conf_class}">{driver["confidence"]} confidence</span>'
      f"{method_badge}"
      f"</div>"
      f'<div style="font-size:0.88rem;color:#475569;line-height:1.5">'
      f"<strong>{driver['contribution_pct']}%</strong> of the movement · "
      f"{driver['evidence']}</div></div>"
    )


def render_evidence_table(evidence_items, show_technical=False):
  rows = ""
  for item in evidence_items:
    source = friendly_source(item["source"])
    method_col = ""
    if show_technical:
      method_col = f'<span class="if-badge if-badge-sql">{item["method"]}</span> '
    rows += (
      f'<div class="if-evidence-row">'
      f'<span class="if-evidence-source">{source}</span>'
      f'<span class="if-evidence-detail">{method_col}{item["detail"]}</span>'
      f'<span class="if-badge if-badge-fresh">{item.get("freshness_label", "Up to date")}</span>'
      f"</div>"
    )
  render_html(
    f'<div class="if-panel" style="padding:0;overflow:hidden">'
    f'<div style="padding:4px 0">{rows}</div></div>'
  )
