import streamlit as st

from auth import show_auth_page
from dashboard import show_dashboard
from expenses_page import show_expenses_page
from other_pages import show_other_pages
from charts import show_charts

st.set_page_config(
    page_title="AI Expense Tracker",
    layout="wide"
)

st.sidebar.title("💰 AI Expense Tracker")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Login",
        "Dashboard",
        "Expenses",
        "Charts",
        "AI Insights"
    ]
)

if menu == "Login":
    show_auth_page()

elif menu == "Dashboard":
    show_dashboard()

elif menu == "Expenses":
    show_expenses_page()

elif menu == "Charts":
    show_charts()

elif menu == "AI Insights":
    show_other_pages()