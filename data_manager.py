import pandas as pd
import os
from datetime import datetime

DATA_FILE = "expenses.csv"

def init_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["date", "category", "amount", "description"])
        df.to_csv(DATA_FILE, index=False)

def load_data():
    init_data()
    return pd.read_csv(DATA_FILE, parse_dates=["date"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def add_expense(date, category, amount, description=""):
    df = load_data()
    new_row = pd.DataFrame([{
        "date": date,
        "category": category,
        "amount": float(amount),
        "description": description
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)

def get_monthly_data(year=None, month=None):
    df = load_data()
    if year and month:
        df = df[(df["date"].dt.year == year) & (df["date"].dt.month == month)]
    return df
