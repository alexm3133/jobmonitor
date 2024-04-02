import streamlit as st
from auth.auth import authenticate_user

def login_page():
    st.title("Iniciar Sesión")
    with st.form("login_form"):
        worker_code = st.text_input("Código de Trabajador", max_chars=10, help="Introduce tu código de trabajador")
        password = st.text_input("Contraseña", type="password", help="Introduce tu contraseña")
        login_button = st.form_submit_button("Iniciar Sesión")
        if login_button:
            if authenticate_user(worker_code, password):
                st.session_state['authenticated'] = True
            else:
                st.error("Código de trabajador o contraseña incorrectos")