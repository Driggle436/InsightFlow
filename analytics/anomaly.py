import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(
    daily_data: pd.DataFrame,
    column: str = "revenue",
) -> pd.DataFrame:

    result = daily_data.copy()

    # Handle empty data - need at least 1 sample for IsolationForest
    if len(result) < 2:
        result["anomaly"] = 1  # Mark as non-anomalous
        result["is_anomaly"] = False
        return result

    model = IsolationForest(
        contamination=0.10,
        random_state=42,
    )

    result["anomaly"] = model.fit_predict(
        result[[column]]
    )

    result["is_anomaly"] = (
        result["anomaly"] == -1
    )

    return result