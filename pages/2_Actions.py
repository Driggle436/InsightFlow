import streamlit as st

from ai.storyteller import generate_story
from components.action_cards import render_action_cards
from components.bento_layout import render_bento_shell
from components.html_render import render_html
from components.layout import render_hero, render_section_header
from utils.bootstrap import load_context, setup_page

setup_page("Actions", "🚀")


def _filter_recs(recommendations, persona_name):
  if persona_name == "CEO":
    return [r for r in recommendations if r["priority"] in ("P1", "P2")]
  if persona_name == "Sales Manager":
    return [r for r in recommendations if "region" in r["title"].lower() or r["priority"] == "P2"]
  return recommendations


def _story_key(persona_name):
  return f"preview_story::{persona_name}"


def _render_persona_tab(persona_name, analysis, show_preview_button=True, tab_id=""):
  st.caption(f"Perspective: **{persona_name}**")

  if show_preview_button:
    if st.button(f"Generate {persona_name} summary", key=f"btn_summary_{persona_name}_{tab_id}"):
      with st.spinner("Generating summary..."):
        try:
          st.session_state[_story_key(persona_name)] = generate_story(
            persona=persona_name,
            revenue_change=analysis["revenue_change"],
            worst_region=analysis["worst_region"],
            worst_change=analysis["worst_change"],
            negative_reviews_count=analysis["negative_count"],
            regional_evidence=analysis["root_causes"],
            review_evidence=analysis["negative_reviews"],
          )
        except Exception as exc:
          st.warning(f"Summary unavailable: {exc}")

  story = st.session_state.get(_story_key(persona_name))
  if story:
    render_html(f'<div class="if-insight-card"><strong>{persona_name} summary</strong></div>')
    st.markdown(story)
  elif show_preview_button:
    st.info("Click the button above to generate a role-specific summary.")

  render_action_cards(_filter_recs(analysis["recommendations"], persona_name), persona_name)


try:
  ctx = load_context()
  persona = ctx["persona"]
  analysis = ctx["analysis"]

  render_bento_shell()
  render_hero(
    "Actions",
    "Prioritized steps by role — who should do what, and expected impact.",
  )

  tab_ceo, tab_sm = st.tabs(["CEO", "Sales Manager"])

  with tab_ceo:
    _render_persona_tab("CEO", analysis, tab_id="ceo_tab")

  with tab_sm:
    _render_persona_tab("Sales Manager", analysis, tab_id="sm_tab")

except Exception as e:
  st.error(f"Unable to load actions: {e}")
