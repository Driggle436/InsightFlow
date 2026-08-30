import time

from dotenv import load_dotenv
from google import genai

from utils.telemetry import record_llm_call

load_dotenv()

import os

api_key = os.getenv("GEMINI_API_KEY")

client = None
if api_key:
  client = genai.Client(api_key=api_key)


def generate_story(
  persona,
  revenue_change,
  worst_region,
  worst_change,
  negative_reviews_count,
  regional_evidence,
  review_evidence,
):
  if not client:
    return _fallback_story(persona, revenue_change, worst_region, worst_change, negative_reviews_count)

  regional_context = regional_evidence.to_string(index=False) if regional_evidence is not None and not regional_evidence.empty else "No regional data"
  customer_voice = review_evidence.to_string(index=False) if review_evidence is not None and not review_evidence.empty else "No review data"

  if persona == "CEO":
    role_instruction = "Focus on strategic business outcomes, revenue risk, and executive actions."
  elif persona == "Sales Manager":
    role_instruction = "Focus on operational actions for your region, customer issues, and immediate sales steps."
  else:
    role_instruction = "Provide detailed analytical narrative with methodology references."

  prompt = f"""
You are an enterprise business intelligence analyst.

Persona: {persona}
Role: {role_instruction}

MAIN KPI SIGNAL
Revenue change: {revenue_change:.1f}%

WORST REGION
Region: {worst_region}
Revenue change: {worst_change:.1f}%

NEGATIVE CUSTOMER REVIEWS
Count: {negative_reviews_count}

REGIONAL BUSINESS CONTEXT
{regional_context}

CUSTOMER VOICE BY PRODUCT
{customer_voice}

TASK
Explain what is happening from the perspective of the selected persona.
Use ONLY the evidence provided above.
Connect revenue performance with CRM churn and customer-review evidence where appropriate.
Do not invent numbers, causes, or business facts.
If the evidence is insufficient or contradictory, explicitly say that the evidence is insufficient.

Provide:
1. What happened
2. Most likely drivers
3. Supporting evidence
4. Business implication
5. Recommended next step
"""

  start = time.perf_counter()
  response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=prompt,
  )
  latency_ms = round((time.perf_counter() - start) * 1000, 1)

  tokens_in = len(prompt.split()) * 2
  tokens_out = len(response.text.split()) * 2
  record_llm_call("gemini-3.1-flash-lite", tokens_in, tokens_out, latency_ms, f"Narrative for {persona}")

  return response.text


def _fallback_story(persona, revenue_change, worst_region, worst_change, negative_reviews_count):
  return f"""**[{persona} Insight — Deterministic Fallback]**

1. **What happened:** Revenue changed {revenue_change:+.1f}% over the analysis period.
2. **Most likely drivers:** The largest regional decline was in {worst_region} ({worst_change:+.1f}%).
3. **Supporting evidence:** {negative_reviews_count} negative customer reviews detected.
4. **Business implication:** Regional performance divergence requires targeted intervention.
5. **Recommended next step:** Investigate {worst_region} operations and delivery pipeline.

*Note: LLM narrative unavailable. This is a deterministic template response.*
"""
