import pandas as pd
import streamlit as st

from config import get_connection

from analytics.anomaly import detect_anomalies
from analytics.contribution import find_root_causes

from ai.sentiment import analyze_reviews

st.set_page_config(
    page_title="InsightFlow AI",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_sales():
    connection = get_connection()

    query = """
        SELECT
            date,
            region,
            product,
            orders,
            revenue,
            marketing_spend
        FROM sales_transactions
        ORDER BY date
    """

    df = pd.read_sql(query, connection)

    connection.close()

    return df

@st.cache_data
def load_reviews():
    connection = get_connection()

    query = """
        SELECT *
        FROM customer_reviews
    """

    reviews = pd.read_sql(query, connection)

    connection.close()

    return reviews

st.title("📊 InsightFlow AI")

st.caption(
    "AI-powered business intelligence and decision support"
)


try:
    sales = load_sales()

    total_revenue = sales["revenue"].sum()
    total_orders = sales["orders"].sum()

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}",
    )

    col2.metric(
        "Total Orders",
        f"{total_orders:,}",
    )

    col3.metric(
        "Average Order Value",
        f"₹{average_order_value:,.0f}",
    )

    st.divider()

    st.subheader("Revenue Trend")

    daily_revenue = (
        sales
        .groupby("date")["revenue"]
        .sum()
        .reset_index()
    )

    st.line_chart(
        daily_revenue.set_index("date")
    )

    st.subheader("Revenue by Region")

    region_revenue = (
        sales
        .groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(region_revenue)

except Exception as e:

    st.error(
        f"Unable to load dashboard data: {e}"
    )

anomaly_data = detect_anomalies(
    daily_revenue,
    "revenue",
)

st.subheader("Detected Anomalies")

st.dataframe(
    anomaly_data[
        anomaly_data["is_anomaly"]
    ]
)
st.subheader("Root Cause Analysis")

root_causes = find_root_causes(sales)

st.dataframe(root_causes)

worst_region = root_causes.index[0]

st.warning(
    f"Biggest revenue decline occurred in **{worst_region}**."
)

st.subheader("Customer Sentiment")

reviews = load_reviews()
reviews = analyze_reviews(reviews)

sentiment_counts = (
    reviews["sentiment"]
    .value_counts()
)

st.bar_chart(sentiment_counts)

negative_reviews = reviews[
    reviews["sentiment"] == "Negative"
]

st.write("Recent Negative Reviews")

st.dataframe(
    negative_reviews[
        ["product", "rating", "review_text"]
    ]
)