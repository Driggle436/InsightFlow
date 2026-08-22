from textblob import TextBlob
import pandas as pd


def analyze_reviews(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Text sentiment score
    df["polarity"] = df["review_text"].apply(
        lambda text: TextBlob(str(text)).sentiment.polarity
    )

    def classify_sentiment(row):
        rating = row["rating"]
        polarity = row["polarity"]

        # Strong rating signal
        if rating <= 2:
            return "Negative"

        if rating >= 4:
            return "Positive"

        # For 3-star reviews, use the actual text
        if polarity > 0.1:
            return "Positive"

        if polarity < -0.1:
            return "Negative"

        return "Neutral"

    df["sentiment"] = df.apply(
        classify_sentiment,
        axis=1,
    )

    return df