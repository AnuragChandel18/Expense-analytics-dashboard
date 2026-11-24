import streamlit as st
import pandas as pd
from pathlib import Path
from expense_manager import ExpenseManager

st.set_page_config(
    page_title="Expense Analytics Dashboard",
    page_icon="💰",
    layout="wide",
)

DATA_FILE = Path("expenses.csv")
manager = ExpenseManager(DATA_FILE)

st.title("💰 Expense Analytics Dashboard")
st.caption("Track, analyze and understand personal spending with Python and CSV.")

# Sidebar
st.sidebar.header("Add Expense")
with st.sidebar.form("add_expense", clear_on_submit=True):
    expense_date = st.date_input("Date", value=pd.Timestamp.today().date())
    category = st.selectbox("Category", manager.categories)
    description = st.text_input("Description")
    amount = st.number_input("Amount (₹)", min_value=0.01, step=50.0)
    submitted = st.form_submit_button("Add Expense", use_container_width=True)

    if submitted:
        try:
            manager.add_expense(expense_date, category, description, amount)
            st.sidebar.success("Expense added.")
            st.rerun()
        except ValueError as exc:
            st.sidebar.error(str(exc))

df = manager.load()

if df.empty:
    st.info("No expenses yet. Add an expense from the sidebar or use the sample CSV included with the project.")
    st.stop()

# Filters
st.subheader("Filters")
c1, c2, c3 = st.columns(3)

with c1:
    min_date = pd.to_datetime(df["date"]).min().date()
    max_date = pd.to_datetime(df["date"]).max().date()
    date_range = st.date_input("Date range", value=(min_date, max_date))

with c2:
    categories = st.multiselect(
        "Category",
        options=manager.categories,
        default=manager.categories,
    )

with c3:
    search = st.text_input("Search description", placeholder="e.g. groceries")

filtered = df.copy()
filtered["date"] = pd.to_datetime(filtered["date"])

if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filtered[
        (filtered["date"].dt.date >= date_range[0]) &
        (filtered["date"].dt.date <= date_range[1])
    ]

filtered = filtered[filtered["category"].isin(categories)]

if search.strip():
    filtered = filtered[
        filtered["description"].str.contains(search.strip(), case=False, na=False)
    ]

# KPIs
total = filtered["amount"].sum()
average = filtered["amount"].mean() if not filtered.empty else 0
median = filtered["amount"].median() if not filtered.empty else 0
count = len(filtered)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Spend", f"₹{total:,.2f}")
k2.metric("Transactions", f"{count:,}")
k3.metric("Average Expense", f"₹{average:,.2f}")
k4.metric("Median Expense", f"₹{median:,.2f}")

if filtered.empty:
    st.warning("No expenses match the selected filters.")
    st.stop()

# Analytics
left, right = st.columns(2)

with left:
    st.subheader("Spend by Category")
    category_df = (
        filtered.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )
    st.bar_chart(category_df.set_index("category"))

with right:
    st.subheader("Monthly Spending")
    monthly_df = (
        filtered.assign(month=filtered["date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["amount"]
        .sum()
        .sort_values("month")
    )
    st.line_chart(monthly_df.set_index("month"))

# Top expenses
st.subheader("Top 5 Expenses")
top5 = filtered.nlargest(5, "amount")[
    ["date", "category", "description", "amount"]
].copy()
top5["date"] = top5["date"].dt.strftime("%Y-%m-%d")
top5["amount"] = top5["amount"].map(lambda x: f"₹{x:,.2f}")
st.dataframe(top5, use_container_width=True, hide_index=True)

# Raw data
with st.expander("View all filtered transactions"):
    display_df = filtered[
        ["id", "date", "category", "description", "amount"]
    ].copy()
    display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
    st.dataframe(display_df, use_container_width=True, hide_index=True)
