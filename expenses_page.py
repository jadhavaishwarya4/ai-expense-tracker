import streamlit as st
from datetime import date

from db_handler import (
    add_expense,
    get_expenses,
    delete_expense
)


def show_expenses_page():

    st.title("💸 Expense Management")

    with st.form("expense_form"):

        amount = st.number_input(
            "Amount",
            min_value=0.0
        )

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Transport",
                "Shopping",
                "Bills",
                "Entertainment",
                "Health",
                "Education",
                "Others"
            ]
        )

        description = st.text_input(
            "Description"
        )

        expense_date = st.date_input(
            "Date",
            value=date.today()
        )

        submit = st.form_submit_button(
            "Add Expense"
        )

        if submit:

            add_expense(
                1,
                amount,
                category,
                description,
                expense_date
            )

            st.success(
                "Expense Added Successfully!"
            )

    st.divider()

    st.subheader("Expense History")

    expenses = get_expenses(1)

    if expenses:

        for expense in expenses:

            col1, col2 = st.columns([5,1])

            with col1:

                st.write(
                    f"₹{expense[1]} | {expense[2]} | {expense[3]} | {expense[4]}"
                )

            with col2:

                if st.button(
                    "Delete",
                    key=expense[0]
                ):

                    delete_expense(expense[0])

                    st.rerun()

    else:

        st.info("No expenses found")