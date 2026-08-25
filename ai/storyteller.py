import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_story(revenue_change, worst_region, worst_change, negative_reviews_count):
    prompt = f"""
    You are an executive business analyst.

    Use these facts only.

    Revenue change: {revenue_change:.1f}%
    Worst-performing region: {worst_region}
    Region decline: {worst_change:.1f}%
    Negative reviews: {negative_reviews_count}

    Write:
    1. Executive summary (2-3 sentences)
    2. Main business risk
    3. Immediate action recommendation

    Keep it under 120 words.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a concise executive business analyst."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content