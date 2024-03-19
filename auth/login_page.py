import streamlit as st
from database.database_connection import create_connection

database = "soldering_db.sqlite"

def authenticate_user(user_code, password):
    """Authenticate a user based on their worker code and password."""
    conn = create_connection(database)  # Crear una nueva conexión
    try:
        sql = '''SELECT * FROM users WHERE trabajador_code=? AND trabajador_password=?'''
        cur = conn.cursor()
        cur.execute(sql, (user_code, password))
        account = cur.fetchone()
        return account is not None
    finally:
        conn.close()  #

def logout():
    st.session_state['authenticated'] = False
    st.experimental_rerun()


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