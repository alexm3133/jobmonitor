import streamlit as st
from database.database_connection import create_connection


database = "soldering_db.sqlite"

def authenticate_user(user_code, password):
    """Authenticate a user based on their worker code, password, and retrieves their priority."""
    conn = create_connection(database)  
    try:
        sql = '''SELECT * FROM users WHERE worker_code=? AND worker_password=?'''
        cur = conn.cursor()
        cur.execute(sql, (user_code, password))
        account = cur.fetchone()
        if account:
            # Assuming 'prioridad' is the 5th column in the 'users' table
            st.session_state['authenticated'] = True
            st.session_state['user_priority'] = account[4]  # adjust the index based on your table structure
            return True
        else:
            return False
    finally:
        conn.close()

def logout():
    st.session_state['authenticated'] = False
    st.experimental_rerun()

