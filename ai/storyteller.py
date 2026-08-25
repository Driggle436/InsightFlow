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
    revenue_change,
    worst_region,
    worst_change,
    negative_reviews_count,
):

    prompt = f"""
You are an executive business analyst for a business intelligence platform.

Analyze the following verified business metrics.

Revenue change:
{revenue_change:.1f}%

Worst-performing region:
{worst_region}

Revenue change in that region:
{worst_change:.1f}%

Number of negative customer reviews:
{negative_reviews_count}

Create a concise executive insight.

Use exactly these sections:

EXECUTIVE SUMMARY
Explain what happened in 2-3 sentences.

BUSINESS RISK
Explain the most important risk.

RECOMMENDED ACTION
Give one practical action management should take.

IMPORTANT:
- Use only the numbers provided.
- Do not invent additional data.
- Do not claim causation that cannot be proven.
- Keep the response under 150 words.
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )

    return response.text