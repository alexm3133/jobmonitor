import sqlite3
from sqlite3 import Error
import pandas as pd
import streamlit as st

# Database setup
def create_connection(db_file):
    """Create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        create_table(conn)
        create_components_table(conn)
    except Error as e:
        st.error(f"Error: {e}")
    return conn

def create_table(conn):
    """Create the soldering_entries table if it doesn't already exist"""
    sql = """CREATE TABLE IF NOT EXISTS soldering_entries (
             id INTEGER PRIMARY KEY,
             worker_name TEXT NOT NULL,
             component_id INTEGER NOT NULL,
             time_spent REAL NOT NULL,
             date TEXT NOT NULL,
             FOREIGN KEY (component_id) REFERENCES components(id)
             );"""
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        st.error(f"Error: {e}")

def create_components_table(conn):
    """Create the components table if it doesn't already exist"""
    sql = """CREATE TABLE IF NOT EXISTS components (
             id INTEGER PRIMARY KEY,
             component_name TEXT NOT NULL,
             component_code TEXT UNIQUE NOT NULL
             );"""
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        st.error(f"Error: {e}")

def add_component(conn, component_name, component_code):
    """Add a new component to the components table"""
    sql = 'INSERT INTO components(component_name, component_code) VALUES(?, ?)'
    try:
        c = conn.cursor()
        c.execute(sql, (component_name, component_code))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("Component code already exists.")
    except Error as e:
        st.error(f"Error adding component: {e}")

def get_components(conn):
    """Fetch all components from the components table"""
    sql = 'SELECT * FROM components'
    try:
        c = conn.cursor()
        c.execute(sql)
        components = c.fetchall()
        return components
    except Error as e:
        st.error(f"Error fetching components: {e}")
        return []

def add_entry(conn, worker_name, component_id, time_spent, date):
    """Add a new entry to the soldering_entries table"""
    sql = '''INSERT INTO soldering_entries(worker_name, component_id, time_spent, date) VALUES(?,?,?,?)'''
    try:
        c = conn.cursor()
        c.execute(sql, (worker_name, component_id, time_spent, date))
        conn.commit()
    except Error as e:
        st.error(f"Error adding entry: {e}")

def get_entries(conn):
    """Fetch all entries from the soldering_entries table"""
    sql = 'SELECT se.id, se.date, se.time_spent, c.component_name, c.component_code, se.worker_name FROM soldering_entries se JOIN components c ON se.component_id = c.id'
    try:
        c = conn.cursor()
        c.execute(sql)
        entries = c.fetchall()
        return entries
    except Error as e:
        st.error(f"Error fetching entries: {e}")
        return []

def delete_entry(conn, entry_id):
    """Delete an entry from the soldering_entries table"""
    sql = 'DELETE FROM soldering_entries WHERE id=?'
    try:
        c = conn.cursor()
        c.execute(sql, (entry_id,))
        conn.commit()
    except Error as e:
        st.error(f"Error deleting entry: {e}")

def update_entry(conn, entry_id, worker_name, component_id, time_spent):
    """Update an existing entry in the soldering_entries table"""
    sql = '''UPDATE soldering_entries SET worker_name=?, component_id=?, time_spent=? WHERE id=?'''
    try:
        c = conn.cursor()
        c.execute(sql, (worker_name, component_id, time_spent, entry_id))
        conn.commit()
    except Error as e:
        st.error(f"Error updating entry: {e}")

def generate_report(conn, start_date, end_date):
    """Generate a report of entries within a specific date range"""
    sql = '''SELECT se.date, se.time_spent, c.component_name, c.component_code, se.worker_name FROM soldering_entries se JOIN components c ON se.component_id = c.id WHERE date BETWEEN ? AND ?'''
    try:
        c = conn.cursor()
        c.execute(sql, (start_date, end_date))
        entries = c.fetchall()
        df = pd.DataFrame(entries, columns=['Date', 'Time Spent', 'Component Name', 'Component Code', 'Worker Name'])
        return df
    except Error as e:
        st.error(f"Error generating report: {e}")
        return pd.DataFrame()


# Main
