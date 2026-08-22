import pandas as pd
import streamlit as st

from config import get_connection

from analytics.anomaly import detect_anomalies
from analytics.contribution import find_root_causes

from ai.sentiment import analyze_reviews


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="InsightFlow AI",
    page_icon="📊",
    layout="wide",
)


# ---------------------------------------------------------
# KPI CALCULATION
# ---------------------------------------------------------

def calculate_kpi_change(daily_data):
    daily_data = daily_data.sort_values("date")

    if len(daily_data) < 20:
        return 0

    previous_period = daily_data.iloc[-20:-10]["revenue"].mean()
    current_period = daily_data.iloc[-10:]["revenue"].mean()

    if previous_period == 0:
        return 0

    change = (
        (current_period - previous_period)
        / previous_period
    ) * 100

    return change


# ---------------------------------------------------------
# LOAD SALES
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# LOAD REVIEWS
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("📊 InsightFlow AI")

st.caption(
    "AI-powered business intelligence and decision support"
)


# ---------------------------------------------------------
# MAIN APPLICATION
# ---------------------------------------------------------

try:

    # -----------------------------------------------------
    # LOAD DATA
    # -----------------------------------------------------

    sales = load_sales()

    if sales.empty:
        st.warning("No sales data found in MySQL.")
        st.stop()


    # -----------------------------------------------------
    # BASIC KPIs
    # -----------------------------------------------------

    total_revenue = sales["revenue"].sum()

    total_orders = sales["orders"].sum()

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )


    # -----------------------------------------------------
    # DAILY REVENUE
    # -----------------------------------------------------

    daily_revenue = (
        sales
        .groupby("date")["revenue"]
        .sum()
        .reset_index()
    )

    revenue_change = calculate_kpi_change(
        daily_revenue
    )


    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}",
        f"{revenue_change:+.1f}%"
    )

    col2.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    col3.metric(
        "Average Order Value",
        f"₹{average_order_value:,.0f}"
    )


    st.divider()


    # -----------------------------------------------------
    # REVENUE TREND
    # -----------------------------------------------------

    st.subheader("Revenue Trend")

    st.line_chart(
        daily_revenue.set_index("date")
    )


    # -----------------------------------------------------
    # REVENUE BY REGION
    # -----------------------------------------------------

    st.subheader("Revenue by Region")

    region_revenue = (
        sales
        .groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(region_revenue)


    # -----------------------------------------------------
    # ANOMALY DETECTION
    # -----------------------------------------------------

    st.subheader("Detected Anomalies")

    anomaly_data = detect_anomalies(
        daily_revenue,
        "revenue",
    )

    anomalies = anomaly_data[
        anomaly_data["is_anomaly"]
    ].copy()

    anomalies["status"] = "🔴 Anomaly Detected"

    anomalies = anomalies[
        ["date", "revenue", "status"]
    ]

    if anomalies.empty:

        st.success(
            "No significant revenue anomalies detected."
        )

    else:

        st.dataframe(
            anomalies,
            use_container_width=True,
            hide_index=True,
        )


    # -----------------------------------------------------
    # ROOT CAUSE ANALYSIS
    # -----------------------------------------------------

    st.subheader("Root Cause Analysis")

    root_causes = find_root_causes(sales)

    display_causes = root_causes.reset_index()

    display_causes = display_causes.rename(
    columns={
        "region": "Region",
        "previous": "Previous Revenue",
        "current": "Current Revenue",
        "change": "Revenue Change",
        "percent_change": "Change %",
    }
    )

    display_causes["Previous Revenue"] = (
        display_causes["Previous Revenue"]
        .round(0)
    )

    display_causes["Current Revenue"] = (
        display_causes["Current Revenue"]
        .round(0)
    )

    display_causes["Revenue Change"] = (
        display_causes["Revenue Change"]
        .round(0)
    )

    display_causes["Change %"] = (
        display_causes["Change %"]
        .round(1)
    )

    st.dataframe(
        display_causes,
        use_container_width=True,
        hide_index=True,
    )

    worst_region = root_causes.index[0]

    worst_change = root_causes.iloc[0]["percent_change"]

    st.warning(
        f"Biggest revenue decline occurred in "
        f"**{worst_region}** "
        f"({worst_change:.1f}%)."
    )


    # -----------------------------------------------------
    # CUSTOMER SENTIMENT
    # -----------------------------------------------------

    st.subheader("Customer Sentiment")

    reviews = load_reviews()

    if reviews.empty:

        st.info(
            "No customer reviews found."
        )

    else:

        reviews = analyze_reviews(reviews)

        sentiment_counts = (
            reviews["sentiment"]
            .value_counts()
        )

        st.bar_chart(
            sentiment_counts
        )


        # -------------------------------------------------
        # NEGATIVE REVIEWS
        # -------------------------------------------------

        st.write(
            "Recent Negative Reviews"
        )

        negative_reviews = reviews[
            reviews["sentiment"] == "Negative"
        ]

        if negative_reviews.empty:

            st.success(
                "No negative reviews found."
            )

        else:

            st.dataframe(
                negative_reviews[
                    [
                        "product",
                        "rating",
                        "review_text"
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )


except Exception as e:

    st.error(
        f"Unable to load dashboard data: {e}"
    )