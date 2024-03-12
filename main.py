import streamlit as st
import sqlite3
from sqlite3 import Error
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

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
database = "soldering_db.sqlite"
conn = create_connection(database)

menu_options = ["Soldering Time Tracker", "Manage Entries", "Generate Report", "Administrar Componentes"]
selected_option = st.sidebar.selectbox("Menu", menu_options)

if selected_option == "Soldering Time Tracker":
    st.title('Soldering Time Tracker')
    worker_name = st.text_input("Worker Name", "")
    components = get_components(conn)
    component_options = {comp[1]: comp[0] for comp in components}  # component_name: component_id
    selected_component = st.selectbox("Component", list(component_options.keys()))
    selected_component_id = component_options[selected_component]
    time_spent = st.number_input("Time Spent (Hours)", min_value=0.0, format="%.2f")
    date = st.date_input("Date", datetime.now())
    if st.button("Submit"):
        add_entry(conn, worker_name, selected_component_id, time_spent, date.strftime("%Y-%m-%d"))
        st.success("Entry added successfully!")

elif selected_option == "Manage Entries":
    st.header("Manage Entries")
    entries = get_entries(conn)
    entries_df = pd.DataFrame(entries, columns=['ID', 'Date', 'Time Spent', 'Component Name', 'Component Code', 'Worker Name'])
    st.dataframe(entries_df)
    entry_id_to_edit_or_delete = st.number_input("Enter ID of entry to edit or delete", min_value=0, format="%d", key="edit_delete")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete", key="delete"):
            delete_entry(conn, entry_id_to_edit_or_delete)
            st.success(f"Entry {entry_id_to_edit_or_delete} deleted successfully!")
    with col2:
        if st.button("Edit", key="edit"):
            pass
elif selected_option == "Generate Report":
    st.header("Generate Report")
    start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    end_date = st.date_input("End Date", datetime.now())
    if st.button("Generate"):
        report_df = generate_report(conn, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        st.dataframe(report_df)
        # Optional: Add visualization code here

elif selected_option == "Administrar Componentes":
    st.header("Administrar Componentes")
    component_name = st.text_input("Nombre del Componente", "")
    component_code = st.text_input("Código del Componente", "")
    if st.button("Añadir Componente"):
        add_component(conn, component_name, component_code)
        st.success("Componente añadido correctamente.")

