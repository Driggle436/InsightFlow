import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing from .env"
    )


client = genai.Client(
    api_key=api_key
)


def generate_story(
    persona,
    revenue_change,
    worst_region,
    worst_change,
    negative_reviews_count,
    regional_evidence,
    review_evidence,
):
    regional_context = regional_evidence.to_string(
    index=False
    )

    customer_voice = review_evidence.to_string(
        index=False
    )

    if persona == "CEO":

        role_instruction = """
        Focus on strategic business outcomes.
        Mention revenue, regional performance,
        business risk, and executive actions.
        """

    else:

        role_instruction = """
        Focus on operational actions.
        Mention the affected region,
        customer issues,
        and immediate sales actions.
        """

    prompt = f"""
You are an enterprise business intelligence analyst.

Persona:
{persona}

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

Explain what is happening from the perspective of the
selected persona.

Use ONLY the evidence provided above.

Connect revenue performance with CRM churn and
customer-review evidence where appropriate.

Do not invent numbers, causes, or business facts.

If the evidence is insufficient or contradictory,
explicitly say that the evidence is insufficient.

Provide:

1. What happened
2. Most likely drivers
3. Supporting evidence
4. Business implication
5. Recommended next step
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )

    return response.text