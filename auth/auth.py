import streamlit as st
from database.database_connection import create_connection


database = "soldering_db.sqlite"

def authenticate_user(user_code, password):
    """Authenticate a user based on their worker code and password."""
    conn = create_connection(database)  
    try:
        sql = '''SELECT * FROM users WHERE trabajador_code=? AND trabajador_password=?'''
        cur = conn.cursor()
        cur.execute(sql, (user_code, password))
        account = cur.fetchone()
        return account is not None
    finally:
        conn.close()  

def logout():
    st.session_state['authenticated'] = False
    st.experimental_rerun()

