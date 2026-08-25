import pandas as pd
import streamlit as st

from config import get_connection

from analytics.anomaly import detect_anomalies
from analytics.contribution import find_root_causes
from analytics.confidence import calculate_confidence

from ai.sentiment import analyze_reviews

from ai.storyteller import generate_story

from ai.recommendations import generate_recommendations

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

st.sidebar.title("InsightFlow Controls")

persona = st.sidebar.selectbox(
    "Choose your role",
    ["CEO", "Sales Manager"]
)

st.sidebar.divider()

st.sidebar.subheader("Dashboard Filters")

# ---------------------------------------------------------
# MAIN APPLICATION
# ---------------------------------------------------------

try:

    # -----------------------------------------------------
    # LOAD DATA
    # -----------------------------------------------------

    sales = load_sales()

    # -----------------------------------------------------
    # FILTERS
    # -----------------------------------------------------

    sales["date"] = pd.to_datetime(sales["date"])

    min_date = sales["date"].min()
    max_date = sales["date"].max()

    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    regions = ["All"] + sorted(sales["region"].unique().tolist())
    selected_region = st.sidebar.selectbox(
        "Region",
        regions,
    )

    products = ["All"] + sorted(sales["product"].unique().tolist())
    selected_product = st.sidebar.selectbox(
        "Product",
        products,
    )

    filtered_sales = sales.copy()

    # Date filter
    if len(date_range) == 2:
        start_date, end_date = date_range

        filtered_sales = filtered_sales[
            (filtered_sales["date"] >= pd.Timestamp(start_date))
            &
            (filtered_sales["date"] <= pd.Timestamp(end_date))
        ]

    # Region filter
    if selected_region != "All":
        filtered_sales = filtered_sales[
            filtered_sales["region"] == selected_region
        ]

    # Product filter
    if selected_product != "All":
        filtered_sales = filtered_sales[
            filtered_sales["product"] == selected_product
        ]

    sales = filtered_sales

    if sales.empty:
        st.warning("No data matches the selected filters.")
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
    st.caption(
    f"Showing: **{selected_region}** | **{selected_product}**"
    )
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

    display_causes = display_causes[
    [
        "Region",
        "Previous Revenue",
        "Current Revenue",
        "Revenue Change",
        "Change %",
    ]
]

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

    # -----------------------------------------------------
    # AI STORYTELLER
    # -----------------------------------------------------

    st.divider()
    st.subheader("🤖 AI Executive Insight")

    negative_count = len(
        reviews[reviews["sentiment"] == "Negative"]
    )

    anomaly_count = len(anomalies)

    # Generate recommendation data
    recommendations = generate_recommendations(
        revenue_change=revenue_change,
        worst_region=worst_region,
        worst_change=worst_change,
        negative_reviews_count=negative_count,
        anomaly_count=anomaly_count,
    )

    # Calculate confidence
    confidence_score, confidence_components = calculate_confidence(
        sales=sales,
        daily_revenue=daily_revenue,
        anomaly_data=anomaly_data,
        root_causes=root_causes,
        negative_reviews_count=negative_count,
    )

    # -----------------------------------------------------
    # INSIGHT CONFIDENCE
    # -----------------------------------------------------

    st.divider()
    st.subheader("🎯 Insight Confidence")

    confidence_col1, confidence_col2 = st.columns([1, 2])

    with confidence_col1:
        st.metric(
            "Confidence Score",
            f"{confidence_score}%"
        )

    with confidence_col2:
        st.write(
            "Confidence is calculated from data freshness, "
            "data completeness, statistical strength, "
            "and supporting evidence."
        )

    st.progress(confidence_score / 100)

    # Confidence Breakdown

    st.write("### Confidence Breakdown")

    confidence_table = pd.DataFrame({
        "Factor": list(confidence_components.keys()),
        "Score": list(confidence_components.values()),
    })

    st.dataframe(
        confidence_table,
        use_container_width=True,
        hide_index=True,
    )

    if confidence_score >= 80:
        st.success(
            "High confidence: the insight is supported by strong and sufficiently complete evidence."
        )
    elif confidence_score >= 60:
        st.warning(
            "Medium confidence: the insight is useful, but additional evidence should be reviewed."
        )
    else:
        st.error(
            "Low confidence: insufficient evidence is available to make a reliable conclusion."
        )

    # -----------------------------------------------------
    # GENERATE AI INSIGHT
    # -----------------------------------------------------

    if st.button("Generate AI Insight"):

        with st.spinner("Analyzing business performance..."):

            try:
                story = generate_story(
                    persona=persona,
                    revenue_change=revenue_change,
                    worst_region=worst_region,
                    worst_change=worst_change,
                    negative_reviews_count=negative_count,
                )

                st.markdown(f"### AI Analysis for {persona}")
                st.info(story)

            except Exception as e:
                st.warning(
                    "Gemini AI is currently unavailable. Showing analytics only."
                )
                st.caption(str(e))

    # -----------------------------------------------------
    # AI ACTION RECOMMENDATIONS
    # -----------------------------------------------------

    st.divider()
    st.subheader("🚀 AI Action Recommendations")

    for rec in recommendations:

        with st.container(border=True):

            st.markdown(
                f"## {rec['priority']} — {rec['title']}"
            )

            col1, col2 = st.columns(2)

            col1.metric("Impact", rec["impact"])
            col2.metric("Effort", rec["effort"])

            st.write(f"**Owner:** {rec['owner']}")

            st.write("**Evidence:**")

            for item in rec["evidence"]:
                st.write(f"• {item}")



except Exception as e:

    st.error(
        f"Unable to load dashboard data: {e}"
    )