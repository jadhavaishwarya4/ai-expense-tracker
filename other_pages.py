import streamlit as st

from prediction import predict_expenses
from chatbot import chatbot_response


def show_other_pages():

    st.title("🤖 AI Insights")

    monthly_data = [12000, 15000, 14000, 17000]

    prediction = predict_expenses(monthly_data)

    st.warning(
        f"Predicted next month expense: ₹{prediction}"
    )

    st.subheader("💬 AI Finance Chatbot")

    question = st.text_input(
        "Ask Finance AI"
    )

    if question:

        answer = chatbot_response(question)

        st.success(answer)