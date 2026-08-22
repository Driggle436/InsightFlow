from textblob import TextBlob
import pandas as pd

def analyze_reviews(df):
    df = df.copy()

    df["polarity"] = df["review_text"].apply(
        lambda x: TextBlob(x).sentiment.polarity
    )

    df["sentiment"] = df["polarity"].apply(
        lambda p: "Positive" if p > 0
        else "Negative" if p < 0
        else "Neutral"
    )

    return df