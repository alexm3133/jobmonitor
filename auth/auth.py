import sqlite3
import bcrypt
import streamlit as st
from database.database_connection import create_connection

database = "soldering_db.sqlite"

def authenticate_user(user_code, password):
    """Authenticate a user based on their worker code and password, and retrieves their priority, using hashed password verification."""
    conn = create_connection(database)
    try:
        sql = '''SELECT worker_password, priority FROM users WHERE worker_code=?'''
        cur = conn.cursor()
        cur.execute(sql, (user_code,))
        result = cur.fetchone()
        if result:
            stored_password_hash, priority = result
            # Verificar la contraseña ingresada con el hash almacenado
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
                st.session_state['authenticated'] = True
                st.session_state['user_priority'] = priority
                return True
        return False
    finally:
        conn.close()

def logout():
    st.session_state['authenticated'] = False
    st.experimental_rerun()

