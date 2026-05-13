import streamlit as st


def show_auth_page():

    st.title("🔐 Login & Signup")

    tab1, tab2 = st.tabs([
        "Login",
        "Signup"
    ])

    with tab1:

        st.subheader("Login")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            st.success(
                f"Welcome {username}!"
            )

    with tab2:

        st.subheader("Create Account")

        new_user = st.text_input(
            "New Username"
        )

        new_email = st.text_input(
            "Email"
        )

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        if st.button("Signup"):

            st.success(
                "Account Created Successfully!"
            )