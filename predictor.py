import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from data_manager import load_data

def predict_next_month():
    df = load_data()
    if len(df) < 3:
        return {}

    df["month"] = df["date"].dt.to_period("M")
    monthly = df.groupby(["month", "category"])["amount"].sum().reset_index()
    monthly["month"] = monthly["month"].dt.to_timestamp()

    predictions = {}
    categories = monthly["category"].unique()

    for cat in categories:
        cat_data = monthly[monthly["category"] == cat].set_index("month")["amount"]
        if len(cat_data) > 1:
            model = ExponentialSmoothing(cat_data, trend="add", seasonal=None)
            fit = model.fit()
            pred = fit.forecast(1).iloc[0]
            predictions[cat] = round(pred, 2)
    
    return predictions
