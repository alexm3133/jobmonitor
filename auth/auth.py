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
            if isinstance(stored_password_hash, str):
                stored_password_hash = stored_password_hash.encode('utf-8')
            if isinstance(password, str):
                password = password.encode('utf-8')
            if bcrypt.checkpw(password, stored_password_hash):
                st.session_state['authenticated'] = True
                st.session_state['user_priority'] = priority
                return True
        return False
    finally:
        conn.close()
        
def register_user(worker_code, worker_name, password):
    conn = create_connection(database)
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE worker_code=?", (worker_code,))
        if cur.fetchone():
            return False 
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        sql = '''INSERT INTO users (worker_code, worker_name, worker_password, priority) VALUES (?, ?, ?, ?)'''
        cur.execute(sql, (worker_code, worker_name, password_hash, 1))  # Asumiendo que todos los nuevos usuarios tienen prioridad 1
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()

def logout():
    st.session_state['authenticated'] = False
    st.experimental_rerun()

