import streamlit as st

from components.html_render import render_html
from utils.telemetry import get_telemetry_summary


def render_telemetry_dashboard():
  summary = get_telemetry_summary()

  render_html(
    f'<div class="if-telemetry-grid">'
    f'<div class="if-telemetry-card"><div class="if-telemetry-value">{summary["llm_calls"]}</div>'
    f'<div class="if-telemetry-label">LLM Calls</div></div>'
    f'<div class="if-telemetry-card"><div class="if-telemetry-value">{summary["total_tokens"]:,}</div>'
    f'<div class="if-telemetry-label">Total Tokens</div></div>'
    f'<div class="if-telemetry-card"><div class="if-telemetry-value">{summary["avg_latency_ms"]}ms</div>'
    f'<div class="if-telemetry-label">Avg Latency</div></div>'
    f'<div class="if-telemetry-card"><div class="if-telemetry-value">${summary["total_cost_usd"]:.4f}</div>'
    f'<div class="if-telemetry-label">Est. Cost</div></div>'
    f'<div class="if-telemetry-card"><div class="if-telemetry-value">{len(summary["pipeline_steps"])}</div>'
    f'<div class="if-telemetry-label">Pipeline Steps</div></div></div>'
  )

  if summary["calls"]:
    st.markdown("#### LLM Call Log")
    for call in reversed(summary["calls"]):
      st.markdown(
        f"- **{call['purpose']}** — `{call['model']}` | "
        f"{call['tokens_in']}+{call['tokens_out']} tokens | "
        f"{call['latency_ms']}ms | ${call['estimated_cost_usd']:.6f}"
      )

  if summary["pipeline_steps"]:
    st.markdown("#### Pipeline Step Timings")
    for step in summary["pipeline_steps"]:
      badge = step["method"].upper()
      st.markdown(
        f"- **{step['step']}** [{badge}] — {step['duration_ms']}ms"
        + (f" — {step['details']}" if step.get("details") else "")
      )
