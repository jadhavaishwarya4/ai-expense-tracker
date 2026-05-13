import streamlit as st
import pandas as pd
import plotly.express as px


def show_charts():

    st.title("📈 Financial Charts")

    df = pd.DataFrame({
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
        df,
        names="Category",
        values="Amount"
    )

    st.plotly_chart(
        pie_chart,
        use_container_width=True
    )

    st.subheader("Category Comparison")

    bar_chart = px.bar(
        df,
        x="Category",
        y="Amount"
    )

    st.plotly_chart(
        bar_chart,
        use_container_width=True
    )