import pandas as pd


def _count_customers(crm):
    if "customer_id" in crm.columns:
        return crm["customer_id"].nunique()
    return len(crm)


def build_unified_evidence(sales, crm, reviews):

    sales_agg = {
        "revenue": ("revenue", "sum"),
        "orders": ("orders", "sum"),
    }
    if "marketing_spend" in sales.columns:
        sales_agg["marketing_spend"] = ("marketing_spend", "sum")

    sales_region = (
        sales
        .groupby("region")
        .agg(**sales_agg)
        .reset_index()
    )

    customer_count_col = (
        ("customer_id", "count")
        if "customer_id" in crm.columns
        else ("churn", "count")
    )

    crm_region = (
        crm
        .groupby("region")
        .agg(
            customers=customer_count_col,
            churned_customers=("churn", "sum"),
            churn_rate=("churn", "mean"),
        )
        .reset_index()
    )

    crm_region["churn_rate"] = crm_region["churn_rate"] * 100

    regional_evidence = sales_region.merge(
        crm_region,
        on="region",
        how="left",
    )

    if reviews.empty:
        review_evidence = pd.DataFrame(
            columns=["product", "review_count", "average_rating", "negative_reviews"]
        )
    elif "sentiment" in reviews.columns:
        review_evidence = (
            reviews
            .groupby("product")
            .agg(
                review_count=("review_text", "count"),
                average_rating=("rating", "mean"),
                negative_reviews=(
                    "sentiment",
                    lambda x: (x == "Negative").sum(),
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

    business_summary = {
        "total_revenue": sales["revenue"].sum(),
        "total_orders": sales["orders"].sum(),
        "total_customers": _count_customers(crm),
        "total_churned_customers": crm["churn"].sum() if not crm.empty else 0,
        "total_reviews": len(reviews),
        "negative_reviews": (
            (reviews["sentiment"] == "Negative").sum()
            if "sentiment" in reviews.columns
            else 0
        ),
    }

    return regional_evidence, review_evidence, business_summary