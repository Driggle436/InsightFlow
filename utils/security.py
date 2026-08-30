PERSONA_ACCESS = {
  "CEO": {
    "regions": ["North", "South", "East", "West"],
    "columns": ["date", "region", "product", "orders", "revenue", "marketing_spend"],
    "can_see_crm_detail": True,
    "can_see_customer_pii": False,
    "insight_depth": "strategic",
    "description": "Full cross-regional view. Revenue and churn aggregated. No customer PII.",
  },
  "Sales Manager": {
    "regions": ["East"],
    "columns": ["date", "region", "product", "orders", "revenue"],
    "can_see_crm_detail": True,
    "can_see_customer_pii": False,
    "insight_depth": "operational",
    "description": "Restricted to East region. Marketing spend hidden. Operational actions only.",
  },
  "Analyst": {
    "regions": ["North", "South", "East", "West"],
    "columns": ["date", "region", "product", "orders", "revenue", "marketing_spend"],
    "can_see_crm_detail": True,
    "can_see_customer_pii": True,
    "insight_depth": "detailed",
    "description": "Full data access including marketing spend and customer-level CRM.",
  },
}


def apply_security_filter(sales, crm, persona):
  access = PERSONA_ACCESS.get(persona, PERSONA_ACCESS["CEO"])
  
  # Filter sales data by allowed regions
  filtered_sales = sales[sales["region"].isin(access["regions"])].copy()
  allowed_cols = [c for c in access["columns"] if c in filtered_sales.columns]
  filtered_sales = filtered_sales[allowed_cols]

  filtered_crm = crm[crm["region"].isin(access["regions"])].copy()
  if not access["can_see_customer_pii"] and "customer_id" in filtered_crm.columns:
    filtered_crm = filtered_crm.drop(columns=["customer_id"])

  return filtered_sales, filtered_crm, access


def get_access_badge(persona):
  access = PERSONA_ACCESS.get(persona, PERSONA_ACCESS["CEO"])
  regions = ", ".join(access["regions"])
  return f"Access: {regions} | Depth: {access['insight_depth']}"
