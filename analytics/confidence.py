import pandas as pd
from datetime import datetime


def calculate_confidence(
    sales,
    daily_revenue,
    anomaly_data,
    root_causes,
    negative_reviews_count,
):
    """
    Calculate a deterministic confidence score
    for the generated business insight.

    Returns:
        total_score
        component_scores
    """

    # -------------------------------------------------
    # 1. DATA FRESHNESS
    # -------------------------------------------------

    latest_date = pd.to_datetime(
        sales["date"]
    ).max()

    today = pd.Timestamp(
        datetime.now().date()
    )

    days_old = (
        today - latest_date
    ).days

    if days_old <= 1:
        freshness = 100

    elif days_old <= 3:
        freshness = 90

    elif days_old <= 7:
        freshness = 75

    elif days_old <= 14:
        freshness = 60

    else:
        freshness = 40


    # -------------------------------------------------
    # 2. DATA COMPLETENESS
    # -------------------------------------------------

    required_columns = [
        "date",
        "region",
        "product",
        "orders",
        "revenue",
        "marketing_spend",
    ]

    available_columns = [
        column
        for column in required_columns
        if column in sales.columns
    ]

    column_score = (
        len(available_columns)
        / len(required_columns)
    ) * 100

    missing_values = (
        sales[available_columns]
        .isna()
        .mean()
        .mean()
    )

    completeness = (
        column_score * 0.7
        + (1 - missing_values) * 100 * 0.3
    )


    # -------------------------------------------------
    # 3. STATISTICAL STRENGTH
    # -------------------------------------------------

    statistical_strength = 50

    if len(daily_revenue) >= 30:
        statistical_strength += 20

    elif len(daily_revenue) >= 20:
        statistical_strength += 10

    anomaly_count = (
        anomaly_data["is_anomaly"]
        .sum()
        if "is_anomaly" in anomaly_data.columns
        else 0
    )

    if anomaly_count > 0:
        statistical_strength += 15

    statistical_strength = min(
        statistical_strength,
        100
    )


    # -------------------------------------------------
    # 4. EVIDENCE QUALITY
    # -------------------------------------------------

    evidence = 40

    # Root cause evidence
    if root_causes is not None and not root_causes.empty:
        evidence += 25

    # Anomaly evidence
    if anomaly_count > 0:
        evidence += 15

    # Customer evidence
    if negative_reviews_count > 0:
        evidence += 20

    evidence = min(
        evidence,
        100
    )


    # -------------------------------------------------
    # 5. FINAL SCORE
    # -------------------------------------------------

    total_score = (
        freshness * 0.25
        + completeness * 0.20
        + statistical_strength * 0.30
        + evidence * 0.25
    )

    total_score = round(
        total_score
    )

    component_scores = {
        "Data Freshness": round(freshness),
        "Data Completeness": round(completeness),
        "Statistical Strength": round(
            statistical_strength
        ),
        "Evidence Quality": round(evidence),
    }

    return total_score, component_scores