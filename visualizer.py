import plotly.express as px
import plotly.graph_objects as go
from data_manager import load_data

def plot_pie_chart(year, month):
    df = load_data()
    df = df[(df["date"].dt.year == year) & (df["date"].dt.month == month)]
    fig = px.pie(df, values="amount", names="category", title=f"Spending - {year}-{month:02d}")
    return fig

def plot_trend():
    df = load_data()
    df["month"] = df["date"].dt.to_period("M").astype(str)
    monthly = df.groupby("month")["amount"].sum().reset_index()
    fig = px.line(monthly, x="month", y="amount", title="Monthly Spending Trend")
    return fig
