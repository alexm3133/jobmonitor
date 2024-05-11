import sqlite3
import bcrypt
import streamlit as st
from database.database_connection import create_connection

database = "soldering_db.sqlite"

def authenticate_user(user_code, password):
    conn = create_connection(database)
    try:
        sql = '''SELECT worker_password, priority FROM users WHERE worker_code=?'''
        cur = conn.cursor()
        cur.execute(sql, (user_code,))
        result = cur.fetchone()
        if result:
            stored_password_hash, priority = result
            # Convert stored password hash to bytes if it is a string
            if isinstance(stored_password_hash, str):
                stored_password_hash = stored_password_hash.encode('utf-8')
            # Convert password to bytes if it is a string
            if isinstance(password, str):
                password = password.encode('utf-8')
            print(f"Stored hash type after conversion: {type(stored_password_hash)}")  # Debugging line for stored_password_hash
            print(f"Password type after conversion: {type(password)}")  # Debugging line for password type
            # Check the encoded password against the stored hash
            if bcrypt.checkpw(password, stored_password_hash):
                st.session_state['authenticated'] = True
                st.session_state['user_priority'] = priority
                return True
        return False
    finally:
        conn.close()







def logout():
    st.session_state['authenticated'] = False
    st.experimental_rerun()

