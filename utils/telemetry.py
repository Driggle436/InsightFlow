import time
from datetime import datetime


def init_telemetry():
  import streamlit as st

  if "telemetry" not in st.session_state:
    st.session_state.telemetry = {
      "llm_calls": 0,
      "total_tokens_in": 0,
      "total_tokens_out": 0,
      "total_latency_ms": 0,
      "calls": [],
      "pipeline_steps": [],
    }


def record_llm_call(model, tokens_in, tokens_out, latency_ms, purpose):
  import streamlit as st

  init_telemetry()
  st.session_state.telemetry["llm_calls"] += 1
  st.session_state.telemetry["total_tokens_in"] += tokens_in
  st.session_state.telemetry["total_tokens_out"] += tokens_out
  st.session_state.telemetry["total_latency_ms"] += latency_ms
  st.session_state.telemetry["calls"].append({
    "timestamp": datetime.now().isoformat(),
    "model": model,
    "tokens_in": tokens_in,
    "tokens_out": tokens_out,
    "latency_ms": latency_ms,
    "purpose": purpose,
    "estimated_cost_usd": estimate_cost(tokens_in, tokens_out, model),
  })


def record_pipeline_step(step_name, method_type, duration_ms, details=""):
  import streamlit as st

  init_telemetry()
  st.session_state.telemetry["pipeline_steps"].append({
    "step": step_name,
    "method": method_type,
    "duration_ms": duration_ms,
    "details": details,
    "timestamp": datetime.now().isoformat(),
  })


def estimate_cost(tokens_in, tokens_out, model):
  rates = {
    "gemini-3.1-flash-lite": (0.0000001, 0.0000004),
    "gemini-2.0-flash": (0.0000001, 0.0000004),
  }
  rate_in, rate_out = rates.get(model, (0.00000015, 0.0000006))
  return round(tokens_in * rate_in + tokens_out * rate_out, 6)


class TimedStep:
  def __init__(self, step_name, method_type, details=""):
    self.step_name = step_name
    self.method_type = method_type
    self.details = details
    self.start = None

  def __enter__(self):
    self.start = time.perf_counter()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    duration_ms = round((time.perf_counter() - self.start) * 1000, 1)
    record_pipeline_step(self.step_name, self.method_type, duration_ms, self.details)


def get_telemetry_summary():
  import streamlit as st

  init_telemetry()
  t = st.session_state.telemetry
  total_cost = sum(c.get("estimated_cost_usd", 0) for c in t["calls"])
  avg_latency = (
    round(t["total_latency_ms"] / t["llm_calls"], 1)
    if t["llm_calls"] > 0
    else 0
  )
  return {
    "llm_calls": t["llm_calls"],
    "total_tokens": t["total_tokens_in"] + t["total_tokens_out"],
    "tokens_in": t["total_tokens_in"],
    "tokens_out": t["total_tokens_out"],
    "avg_latency_ms": avg_latency,
    "total_cost_usd": round(total_cost, 4),
    "pipeline_steps": t["pipeline_steps"],
    "calls": t["calls"],
  }
