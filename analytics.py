from data_manager import get_monthly_data

BUDGETS = {
    "Food": 6000,
    "Transport": 2000,
    "Entertainment": 3000,
    "Shopping": 4000,
    "Bills": 5000
}

def check_overspending(year, month):
    df = get_monthly_data(year, month)
    spending = df.groupby("category")["amount"].sum().to_dict()
    alerts = []
    tips = []

    for cat, spent in spending.items():
        budget = BUDGETS.get(cat, 3000)
        if spent > budget * 0.8:
            alerts.append(f"{cat}: {spent}/₹{budget} ({spent/budget*100:.0f}%)")
            if cat == "Food":
                tips.append("Cook 3 meals/week to save ₹1,200")
            elif cat == "Entertainment":
                tips.append("Try free events or streaming deals")

    return alerts, tips
