import streamlit as st

from analytics.feedback import save_feedback
from components.bento_layout import render_bento_shell
from components.layout import render_hero, render_section_header
from utils.bootstrap import load_context, setup_page
from utils.data_loader import load_feedback_history

setup_page("Feedback", "📝")

try:
  ctx = load_context()
  persona = ctx["persona"]
  analysis = ctx["analysis"]

  render_bento_shell()
  render_hero(
    "Feedback",
    "Help us improve — correct the insight, add context the data doesn't capture.",
  )

  col1, col2, col3 = st.columns(3)
  col1.metric("Revenue change", f"{analysis['revenue_change']:+.1f}%")
  col2.metric("Confidence", f"{analysis['confidence_score']}%")
  col3.metric("Drivers found", len(analysis["drivers"]))

  render_section_header("Your review")

  feedback_rating = st.radio(
    "Was this insight useful?",
    ["Helpful", "Partially Helpful", "Not Helpful", "Incorrect"],
    horizontal=True,
  )

  feedback_category = st.multiselect(
    "What could be better?",
    [
      "Wrong root cause",
      "Missing business context",
      "Confidence too high",
      "Confidence too low",
      "Wrong region or product",
      "Actions not relevant",
    ],
  )

  feedback_text = st.text_area(
    "What should we know?",
    placeholder="Example: East revenue dropped because of a warehouse move — not in the data yet.",
    height=120,
  )

  if st.button("Submit feedback", type="primary"):
    feedback_text = " ".join(feedback_text.split())
    if not feedback_text.strip():
      st.warning("Please add a correction or context.")
    else:
      category_note = f" [{', '.join(feedback_category)}]" if feedback_category else ""
      try:
        save_feedback(
          persona=persona,
          insight_text=st.session_state.get("generated_story", "No summary generated."),
          rating=feedback_rating,
          correction=feedback_text + category_note,
          confidence_score=int(analysis["confidence_score"]),
        )
        st.success("Thanks — your feedback helps calibrate future insights.")
        load_feedback_history.clear()
      except Exception as e:
        st.error(f"Could not save feedback: {e}")

  render_section_header("Past feedback")
  history = load_feedback_history()
  if history.empty:
    st.info("No feedback yet.")
  else:
    st.dataframe(history, use_container_width=True, hide_index=True)
    helpful = len(history[history["rating"].isin(["Helpful", "Partially Helpful"])])
    total = len(history)
    if total > 0:
      c1, c2 = st.columns(2)
      c1.metric("Helpful rate", f"{helpful / total * 100:.0f}%")
      c2.metric("Submissions", total)

except Exception as e:
  st.error(f"Unable to load feedback: {e}")
