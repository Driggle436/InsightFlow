import pandas as pd

def find_root_causes(sales_df):
    # Compare last 10 days with previous 10 days
    sales_df["date"] = pd.to_datetime(sales_df["date"])

    dates = sorted(sales_df["date"].unique())

    last_period = dates[-10:]
    previous_period = dates[-20:-10]

    last = sales_df[sales_df["date"].isin(last_period)]
    previous = sales_df[sales_df["date"].isin(previous_period)]

    comparison = (
        pd.concat([
            previous.groupby("region")["revenue"].sum().rename("previous"),
            last.groupby("region")["revenue"].sum().rename("current")
        ], axis=1)
        .fillna(0)
    )

    comparison["change"] = comparison["current"] - comparison["previous"]
    comparison["percent_change"] = (
        comparison["change"] / comparison["previous"] * 100
    )

    return comparison.sort_values("change")