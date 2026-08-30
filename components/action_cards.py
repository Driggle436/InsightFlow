import streamlit as st

from components.html_render import render_html

PRIORITY_BADGES = {"P1": "if-badge-p1", "P2": "if-badge-p2", "P3": "if-badge-p3"}
PRIORITY_LABELS = {"P1": "Urgent", "P2": "Important", "P3": "Monitor"}


def render_action_cards(recommendations, persona):
  if not recommendations:
    st.info("All KPIs are within normal range. No actions needed right now.")
    return

  for rec in recommendations:
    badge = PRIORITY_BADGES.get(rec["priority"], "if-badge-p3")
    priority_label = PRIORITY_LABELS.get(rec["priority"], rec["priority"])
    owner = rec["owner"]
    if persona == "CEO" and "Regional" in owner:
      owner = "VP Sales"
    elif persona == "Sales Manager":
      owner = "Your team"

    render_html(
      f'<div class="if-action-card">'
      f'<div class="if-action-header">'
      f'<span class="if-badge {badge}">{priority_label}</span>'
      f'<span class="if-action-title">{rec["title"]}</span>'
      f"</div>"
      f'<div class="if-action-chain">'
      f'<div class="if-action-step"><div class="if-action-step-label">Impact</div>'
      f'<div class="if-action-step-value">{rec["impact"]}</div></div>'
      f'<div class="if-action-step"><div class="if-action-step-label">Effort</div>'
      f'<div class="if-action-step-value">{rec["effort"]}</div></div>'
      f'<div class="if-action-step"><div class="if-action-step-label">Owner</div>'
      f'<div class="if-action-step-value">{owner}</div></div>'
      f'<div class="if-action-step"><div class="if-action-step-label">Confidence</div>'
      f'<div class="if-action-step-value">{rec.get("confidence", "Medium")}</div></div>'
      f"</div></div>"
    )
