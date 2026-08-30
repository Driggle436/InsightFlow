USER_DRIVER_LABELS = {
  "Contribution Analysis": "Sales trends",
  "CRM Aggregation": "Customer retention",
  "Sentiment Analysis (TextBlob)": "Customer feedback",
  "IsolationForest (sklearn)": "Pattern detection",
}

SOURCE_LABELS = {
  "ERP / Sales DB": "Sales",
  "CRM System": "Customers",
  "Review Platform": "Reviews",
  "Review Platform API": "Reviews",
}


def friendly_method(method):
  return USER_DRIVER_LABELS.get(method, "Business data")


def friendly_source(source):
  return SOURCE_LABELS.get(source, source)


def friendly_alert_detail(detail):
  return (
    detail.replace("IsolationForest flagged unusual daily patterns", "Unusual daily patterns detected")
    .replace("IsolationForest", "Analytics engine")
  )
