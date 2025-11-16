import streamlit as st
import pandas as pd
from datetime import datetime
from data_manager import add_expense, load_data, get_monthly_data
from predictor import predict_next_month
from analytics import check_overspending, BUDGETS
from visualizer import plot_pie_chart, plot_trend

st.set_page_config(page_title="Smart Finance Manager", layout="wide")
st.title("💰 Smart Personal Finance Manager")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Add Expense", "Dashboard", "Predictions", "Tips"])

with tab1:
    st.header("Add New Expense")
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date", datetime.today())
        category = st.selectbox("Category", list(BUDGETS.keys()))
    with col2:
        amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
        desc = st.text_input("Description (optional)")

    if st.button("Add Expense"):
        add_expense(date, category, amount, desc)
        st.success(f"Added ₹{amount} to {category}")

with tab2:
    st.header("Monthly Dashboard")
    today = datetime.today()
    year, month = st.selectbox("Year", [2025, 2024], index=0), st.selectbox("Month", range(1,13), index=today.month-1)

    df = get_monthly_data(year, month)
    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_pie_chart(year, month), use_container_width=True)
        with col2:
            st.plotly_chart(plot_trend(), use_container_width=True)

        st.subheader("Summary")
        total = df["amount"].sum()
        st.metric("Total Spent", f"₹{total:,.2f}")
    else:
        st.info("No expenses recorded yet.")

with tab3:
    st.header("Next Month Prediction")
    preds = predict_next_month()
    if preds:
        pred_df = pd.DataFrame(list(preds.items()), columns=["Category", "Predicted (₹)"])
        st.table(pred_df)
    else:
        st.warning("Need more data for predictions")

with tab4:
    st.header("Alerts & Saving Tips")
    alerts, tips = check_overspending(today.year, today.month)
    for alert in alerts:
        st.warning(f"⚠️ {alert}")
    for tip in tips:
        st.info(f"💡 {tip}")
