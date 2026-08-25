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
):

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
You are an AI business analyst.

Role:
{persona}

Instructions:
{role_instruction}

Verified data:

Revenue change:
{revenue_change:.1f}%

Worst region:
{worst_region}

Regional decline:
{worst_change:.1f}%

Negative reviews:
{negative_reviews_count}

Keep the response under 120 words.
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )

    return response.text