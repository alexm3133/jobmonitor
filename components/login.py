import streamlit as st
from auth.auth import authenticate_user

def login_page():
    st.title("Login Page")
    with st.form("login_form"):
        trabajador_code = st.text_input("Worker Code")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        if login_button:
            if authenticate_user(trabajador_code, password):
                st.session_state['authenticated'] = True
            else:
                st.error("Invalid credentials")