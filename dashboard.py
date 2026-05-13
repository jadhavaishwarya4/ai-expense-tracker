import streamlit as st
import pandas as pd
import plotly.express as px

from ai_features import (
    generate_insights,
    financial_health_score,
    savings_recommendations
)

from db_handler import (
    get_total_expenses,
    get_total_income
)


def show_dashboard():

    total_expenses = get_total_expenses()

    total_income = get_total_income()

    savings = total_income - total_expenses

    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Expenses",
        f"₹{total_expenses}"
    )

    col2.metric(
        "Total Income",
        f"₹{total_income}"
    )

    col3.metric(
        "Savings",
        f"₹{savings}"
    )

    chart_data = pd.DataFrame({
        "Category": [
            "Food",
            "Shopping",
            "Bills",
            "Transport",
            "Entertainment"
        ],
        "Amount": [
            4000,
            2500,
            3000,
            1500,
            1500
        ]
    })

    st.subheader("Expense Distribution")

    pie_chart = px.pie(
        chart_data,
        names="Category",
        values="Amount"
    )

    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )

    st.subheader("🤖 AI Insights")

    insights = generate_insights(chart_data)

    for item in insights:
        st.info(item)

    score = financial_health_score(
        total_income,
        total_expenses
    )

    st.subheader("🏆 Financial Health Score")

    st.progress(score)

    st.success(f"Score: {score}/100")

    recommendations = savings_recommendations(
        total_expenses
    )

    st.subheader("💡 Savings Recommendations")

    for rec in recommendations:
        st.warning(rec)