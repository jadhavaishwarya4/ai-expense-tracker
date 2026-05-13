import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px


def show_charts():

    st.title("📈 Financial Charts")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="newpassword123",
        database="expense_tracker"
    )

    query = """
    SELECT category, SUM(amount) as total
    FROM expenses
    GROUP BY category
    """

    df = pd.read_sql(query, conn)

    if not df.empty:

        st.subheader("Expense Distribution")

        pie_chart = px.pie(
            df,
            names="category",
            values="total",
            title="Expense Distribution"
        )

        st.plotly_chart(
            pie_chart,
            use_container_width=True
        )

        st.subheader("Category Comparison")

        bar_chart = px.bar(
            df,
            x="category",
            y="total",
            title="Category Comparison"
        )

        st.plotly_chart(
            bar_chart,
            use_container_width=True
        )

    else:

        st.warning("No expense data found")