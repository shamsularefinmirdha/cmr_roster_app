import streamlit as st

def check_login():
    st.sidebar.title("🔐 Login")

    users = {
        "admin@example.com": {"password": "admin123", "role": "admin"},
        "staff@example.com": {"password": "staff123", "role": "viewer"},
    }

    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        user = users.get(email)
        if user and user["password"] == password:
            st.session_state["role"] = user["role"]
            return user["role"]
        else:
            st.error("Invalid login credentials")
            return None
    return st.session_state.get("role", None)