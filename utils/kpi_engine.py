import pandas as pd

from analytics.anomaly import detect_anomalies
from analytics.contribution import find_root_causes
from analytics.confidence import calculate_confidence
from analytics.evidence import build_unified_evidence
from ai.sentiment import analyze_reviews
from ai.recommendations import generate_recommendations
from utils.semantic_contract import KPI_CONTRACTS
from utils.telemetry import TimedStep


def calculate_kpi_change(daily_data):
  daily_data = daily_data.sort_values("date")
  if len(daily_data) < 20:
    return 0
  previous_period = daily_data.iloc[-20:-10]["revenue"].mean()
  current_period = daily_data.iloc[-10:]["revenue"].mean()
  if previous_period == 0:
    return 0
  return ((current_period - previous_period) / previous_period) * 100


def calculate_orders_change(daily_orders):
  daily_orders = daily_orders.sort_values("date")
  if len(daily_orders) < 20:
    return 0
  prev = daily_orders.iloc[-20:-10]["orders"].mean()
  curr = daily_orders.iloc[-10:]["orders"].mean()
  if prev == 0:
    return 0
  return ((curr - prev) / prev) * 100


def calculate_aov_change(sales):
  sales = sales.copy()
  sales["date"] = pd.to_datetime(sales["date"])
  dates = sorted(sales["date"].unique())
  if len(dates) < 20:
    return 0
  last = sales[sales["date"].isin(dates[-10:])]
  prev = sales[sales["date"].isin(dates[-20:-10])]
  prev_aov = prev["revenue"].sum() / max(prev["orders"].sum(), 1)
  curr_aov = last["revenue"].sum() / max(last["orders"].sum(), 1)
  if prev_aov == 0:
    return 0
  return ((curr_aov - prev_aov) / prev_aov) * 100


def calculate_churn_rate(crm):
  if crm.empty:
    return 0, True
  return round(crm["churn"].mean() * 100, 1), False


def calculate_sparse_product_change(sales):
  """Find and analyze the product with the least historical data (sparse/newest product)"""
  if sales.empty:
    return 0, True, 0, "N/A"
  
  # Find product with least data
  product_days = sales.groupby("product")["date"].nunique()
  if product_days.empty:
    return 0, True, 0, "N/A"
  
  sparse_product = product_days.idxmin()
  sparse_days = product_days.min()
  
  # If all products have enough history, return no sparse product
  if sparse_days >= 30:
    return 0, True, sparse_days, sparse_product
  
  product_sales = sales[sales["product"] == sparse_product].copy()
  daily = product_sales.groupby("date")["revenue"].sum().reset_index().sort_values("date")
  
  if len(daily) < 10:
    return 0, True, sparse_days, sparse_product
  
  prev = daily.iloc[: len(daily) // 2]["revenue"].mean()
  curr = daily.iloc[len(daily) // 2 :]["revenue"].mean()
  
  if prev == 0:
    return 0, True, sparse_days, sparse_product
  
  return ((curr - prev) / prev) * 100, False, sparse_days, sparse_product


def is_material(change_pct, kpi_id):
  contract = next((k for k in KPI_CONTRACTS if k["kpi_id"] == kpi_id), None)
  if not contract:
    return abs(change_pct) >= 5
  thresholds = contract["thresholds"]
  return change_pct >= thresholds["material_up"] or change_pct <= thresholds["material_down"]


def rank_drivers(root_causes, reviews, crm, anomaly_count):
  drivers = []

  if root_causes is not None and not root_causes.empty:
    worst = root_causes.iloc[0]
    drivers.append({
      "driver": f"Regional decline: {root_causes.index[0]}",
      "contribution_pct": round(abs(worst["percent_change"]), 1),
      "method": "Regional analysis",
      "method_type": "stats",
      "confidence": "High" if abs(worst["percent_change"]) > 5 else "Medium",
      "evidence": f"{root_causes.index[0]} revenue changed {worst['percent_change']:.1f}%",
    })

  if crm is not None and not crm.empty:
    churn_by_region = crm.groupby("region")["churn"].mean()
    worst_churn_region = churn_by_region.idxmax()
    churn_rate = churn_by_region.max() * 100
    if churn_rate > 10:
      drivers.append({
        "driver": f"CRM churn spike: {worst_churn_region}",
        "contribution_pct": round(churn_rate, 1),
        "method": "Customer retention",
        "method_type": "sql",
        "confidence": "Medium",
        "evidence": f"{worst_churn_region} churn rate at {churn_rate:.1f}%",
      })

  neg_reviews = reviews[reviews.get("sentiment", pd.Series()) == "Negative"] if "sentiment" in reviews.columns else pd.DataFrame()
  if len(neg_reviews) >= 2:
    top_product = neg_reviews["product"].mode().iloc[0] if not neg_reviews.empty else "Unknown"
    drivers.append({
      "driver": f"Customer dissatisfaction: {top_product}",
      "contribution_pct": round(len(neg_reviews) / max(len(reviews), 1) * 100, 1),
      "method": "Customer feedback",
      "method_type": "ml",
      "confidence": "Medium",
      "evidence": f"{len(neg_reviews)} negative reviews, mostly {top_product}",
    })

  if anomaly_count > 0:
    drivers.append({
      "driver": "Unusual revenue pattern detected",
      "contribution_pct": round(anomaly_count * 5, 1),
      "method": "Pattern detection",
      "method_type": "ml",
      "confidence": "High",
      "evidence": f"{anomaly_count} unusual days in the revenue trend",
    })

  drivers.sort(key=lambda d: d["contribution_pct"], reverse=True)
  return drivers


def run_full_analysis(sales, reviews, crm):
  # Handle empty sales data
  if sales.empty:
    raise ValueError("No sales data available. Please run seed_data.py to populate the database.")
  
  with TimedStep("KPI Calculation", "sql", "Aggregate revenue, orders, AOV"):
    daily_revenue = sales.groupby("date")["revenue"].sum().reset_index()
    daily_orders = sales.groupby("date")["orders"].sum().reset_index()
    
    # Handle case where groupby returns empty dataframe
    if daily_revenue.empty:
      raise ValueError("No daily revenue data. Ensure dates are properly formatted in database.")
    
    revenue_change = calculate_kpi_change(daily_revenue)
    orders_change = calculate_orders_change(daily_orders)
    aov_change = calculate_aov_change(sales)
    churn_rate, churn_sparse = calculate_churn_rate(crm)
    hp_change, hp_sparse, hp_days, sparse_product = calculate_sparse_product_change(sales)

  with TimedStep("Anomaly Detection", "ml", "IsolationForest on daily revenue"):
    anomaly_data = detect_anomalies(daily_revenue, "revenue")
    anomalies = anomaly_data[anomaly_data["is_anomaly"]]
    anomaly_count = len(anomalies)

  with TimedStep("Root Cause Analysis", "stats", "Regional period-over-period comparison"):
    root_causes = find_root_causes(sales)

  with TimedStep("Sentiment Analysis", "ml", "TextBlob polarity scoring"):
    analyzed_reviews = analyze_reviews(reviews) if not reviews.empty else reviews
    negative_count = (
      len(analyzed_reviews[analyzed_reviews["sentiment"] == "Negative"])
      if "sentiment" in analyzed_reviews.columns
      else 0
    )

  with TimedStep("Evidence Reconciliation", "sql", "Merge sales + CRM + reviews"):
    if not crm.empty:
      regional_evidence, review_evidence, business_summary = build_unified_evidence(
        sales, crm, analyzed_reviews
      )
    else:
      regional_evidence, review_evidence, business_summary = pd.DataFrame(), pd.DataFrame(), {}

  worst_region = root_causes.index[0] if not root_causes.empty else "N/A"
  worst_change = root_causes.iloc[0]["percent_change"] if not root_causes.empty else 0

  with TimedStep("Confidence Scoring", "rules", "Weighted freshness + completeness + evidence"):
    confidence_score, confidence_components = calculate_confidence(
      sales=sales,
      daily_revenue=daily_revenue,
      anomaly_data=anomaly_data,
      root_causes=root_causes,
      negative_reviews_count=negative_count,
    )

  with TimedStep("Action Generation", "rules", "Business rule engine for P1-P3 actions"):
    recommendations = generate_recommendations(
      revenue_change=revenue_change,
      worst_region=worst_region,
      worst_change=worst_change,
      negative_reviews_count=negative_count,
      anomaly_count=anomaly_count,
    )

  drivers = rank_drivers(root_causes, analyzed_reviews, crm, anomaly_count)

  kpis = [
    {
      "id": "total_revenue",
      "name": "Total Revenue",
      "value": sales["revenue"].sum(),
      "format": "currency",
      "change": revenue_change,
      "material": is_material(revenue_change, "total_revenue"),
      "sparse": False,
    },
    {
      "id": "total_orders",
      "name": "Total Orders",
      "value": sales["orders"].sum(),
      "format": "number",
      "change": orders_change,
      "material": is_material(orders_change, "total_orders"),
      "sparse": False,
    },
    {
      "id": "aov",
      "name": "Avg Order Value",
      "value": sales["revenue"].sum() / max(sales["orders"].sum(), 1),
      "format": "currency",
      "change": aov_change,
      "material": is_material(aov_change, "aov"),
      "sparse": False,
    },
    {
      "id": "churn_rate",
      "name": "Churn Rate",
      "value": churn_rate,
      "format": "percent",
      "change": 0,
      "material": churn_rate > 15,
      "sparse": churn_sparse,
    },
    {
      "id": "new_product_revenue",
      "name": f"{sparse_product} Revenue",
      "value": sales[sales["product"] == sparse_product]["revenue"].sum(),
      "format": "currency",
      "change": hp_change,
      "material": is_material(hp_change, "new_product_revenue"),
      "sparse": hp_sparse,
      "history_days": hp_days,
    },
  ]

  negative_reviews = (
    analyzed_reviews[analyzed_reviews["sentiment"] == "Negative"]
    if "sentiment" in analyzed_reviews.columns
    else pd.DataFrame()
  )

  return {
    "kpis": kpis,
    "daily_revenue": daily_revenue,
    "daily_orders": daily_orders,
    "revenue_change": revenue_change,
    "anomaly_data": anomaly_data,
    "anomalies": anomalies,
    "anomaly_count": anomaly_count,
    "root_causes": root_causes,
    "worst_region": worst_region,
    "worst_change": worst_change,
    "analyzed_reviews": analyzed_reviews,
    "negative_count": negative_count,
    "negative_reviews": negative_reviews,
    "regional_evidence": regional_evidence,
    "review_evidence": review_evidence,
    "business_summary": business_summary,
    "confidence_score": confidence_score,
    "confidence_components": confidence_components,
    "recommendations": recommendations,
    "drivers": drivers,
  }
