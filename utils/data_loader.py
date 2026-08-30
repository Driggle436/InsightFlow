import pandas as pd
import streamlit as st

from config import get_connection


@st.cache_data(ttl=60)  # Reduced TTL to 60 seconds for dev testing
def load_sales():
  connection = get_connection()
  query = """
    SELECT date, region, product, orders, revenue, marketing_spend
    FROM sales_transactions
    ORDER BY date
  """
  df = pd.read_sql(query, connection)
  connection.close()
  df["date"] = pd.to_datetime(df["date"])
  return df


@st.cache_data(ttl=300)
def load_reviews():
  connection = get_connection()
  query = "SELECT * FROM customer_reviews"
  reviews = pd.read_sql(query, connection)
  connection.close()
  return reviews


@st.cache_data(ttl=300)
def load_crm():
  connection = get_connection()
  query = "SELECT customer_id, region, churn, signup_date FROM crm_customers"
  crm = pd.read_sql(query, connection)
  connection.close()
  return crm


@st.cache_data(ttl=60)
def load_feedback_history():
  connection = get_connection()
  query = """
    SELECT feedback_id, persona, rating, correction, confidence_score, created_at
    FROM insight_feedback
    ORDER BY created_at DESC
    LIMIT 50
  """
  try:
    df = pd.read_sql(query, connection)
  except Exception:
    df = pd.DataFrame()
  connection.close()
  return df


def apply_filters(sales, date_range, region, product):
  filtered = sales.copy()
  if len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
      (filtered["date"] >= pd.Timestamp(start_date))
      & (filtered["date"] <= pd.Timestamp(end_date))
    ]
  if region != "All":
    filtered = filtered[filtered["region"] == region]
  if product != "All":
    filtered = filtered[filtered["product"] == product]
  return filtered


def get_filter_options(sales):
  min_date = sales["date"].min()
  max_date = sales["date"].max()
  regions = ["All"] + sorted(sales["region"].unique().tolist())
  products = ["All"] + sorted(sales["product"].unique().tolist())
  return min_date, max_date, regions, products
