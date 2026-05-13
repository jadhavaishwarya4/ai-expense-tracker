import streamlit as st
import pandas as pd
import mysql.connector
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

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="newpassword123",
        database="expense_tracker"
    )

    query = '''
    SELECT category, SUM(amount) as total
    FROM expenses
    GROUP BY category
    '''

    df = pd.read_sql(query, conn)

    if not df.empty:

        fig = px.pie(
            df,
            names='category',
            values='total',
            title='Expense Distribution'
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("🤖 AI Insights")

    expense_df = pd.read_sql(
        "SELECT * FROM expenses",
        conn
    )

    insights = generate_insights(expense_df)

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