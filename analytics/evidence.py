import pandas as pd


def build_unified_evidence(sales, crm, reviews):

    # -------------------------------------------------
    # 1. SALES BY REGION
    # -------------------------------------------------

    sales_region = (
        sales
        .groupby("region")
        .agg(
            revenue=("revenue", "sum"),
            orders=("orders", "sum"),
            marketing_spend=("marketing_spend", "sum"),
        )
        .reset_index()
    )

    # -------------------------------------------------
    # 2. CRM BY REGION
    # -------------------------------------------------

    crm_region = (
        crm
        .groupby("region")
        .agg(
            customers=("customer_id", "count"),
            churned_customers=("churn", "sum"),
            churn_rate=("churn", "mean"),
        )
        .reset_index()
    )

    crm_region["churn_rate"] = (
        crm_region["churn_rate"] * 100
    )

    # -------------------------------------------------
    # 3. RECONCILE SALES + CRM
    # -------------------------------------------------

    regional_evidence = sales_region.merge(
        crm_region,
        on="region",
        how="left",
    )

    # -------------------------------------------------
    # 4. REVIEWS BY PRODUCT
    # -------------------------------------------------

    if "sentiment" in reviews.columns:

        review_evidence = (
            reviews
            .groupby("product")
            .agg(
                review_count=("review_text", "count"),
                average_rating=("rating", "mean"),
                negative_reviews=(
                    "sentiment",
                    lambda x: (x == "Negative").sum()
                ),
            )
            .reset_index()
        )

    else:

        review_evidence = (
            reviews
            .groupby("product")
            .agg(
                review_count=("review_text", "count"),
                average_rating=("rating", "mean"),
            )
            .reset_index()
        )

        review_evidence["negative_reviews"] = 0

    # -------------------------------------------------
    # 5. BUSINESS SUMMARY
    # -------------------------------------------------

    business_summary = {
        "total_revenue": sales["revenue"].sum(),
        "total_orders": sales["orders"].sum(),
        "total_customers": crm["customer_id"].nunique(),
        "total_churned_customers": crm["churn"].sum(),
        "total_reviews": len(reviews),
        "negative_reviews": (
            (reviews["sentiment"] == "Negative").sum()
            if "sentiment" in reviews.columns
            else 0
        ),
    }

    return (
        regional_evidence,
        review_evidence,
        business_summary,
    )