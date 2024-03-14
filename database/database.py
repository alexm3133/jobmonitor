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
        create_trabajador_table(conn)
        create_component_codifications_table(conn)
    except Error as e:
        st.error(f"Error: {e}")
    return conn

def create_table(conn):
    """Create or modify the soldering_entries table to include new fields."""
    sql = """CREATE TABLE IF NOT EXISTS soldering_entries (
             id INTEGER PRIMARY KEY,
             worker_name TEXT NOT NULL,
             component_id INTEGER NOT NULL,
             time_spent REAL NOT NULL,
             date TEXT NOT NULL,
             codification TEXT,  -- New column for codification
             quantity INTEGER NOT NULL DEFAULT 1,  -- New column for quantity
             start_time TEXT,  -- New column for start time
             end_time TEXT,  -- New column for end time
             FOREIGN KEY (component_id) REFERENCES components(id),
             FOREIGN KEY (worker_name) REFERENCES users(trabajador_code)
             );"""
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        st.error(f"Error: {e}")
def create_component_codifications_table(conn):
    """Create the component_codifications table if it doesn't already exist"""
    sql = """CREATE TABLE IF NOT EXISTS component_codifications (
             id INTEGER PRIMARY KEY,
             component_id INTEGER NOT NULL,
             codification TEXT NOT NULL,
             FOREIGN KEY (component_id) REFERENCES components(id)
             );"""
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        st.error(f"Error creating component_codifications table: {e}")


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

def create_trabajador_table(conn):
    """Create the users table if it doesn't already exist"""
    sql = """CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY,
             trabajador_name TEXT NOT NULL,
             trabajador_code TEXT UNIQUE NOT NULL
             );"""
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        st.error(f"Error: {e}")
        
def add_trabajador(conn, trabajador_name, trabajador_code):
    """Add a new user to the users table"""
    sql = 'INSERT INTO users(trabajador_name, trabajador_code) VALUES(?, ?)'
    try:
        c = conn.cursor()
        c.execute(sql, (trabajador_name, trabajador_code))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("Trabajador code already exists.")
    except Error as e:
        st.error(f"Error adding trabajador: {e}")
def add_component(conn, component_name, component_code):
    """Add a new component to the components table and return its ID."""
    sql = 'INSERT INTO components(component_name, component_code) VALUES(?, ?)'
    try:
        c = conn.cursor()
        c.execute(sql, (component_name, component_code))
        conn.commit()
        return c.lastrowid  # Devuelve el ID del nuevo componente
    except sqlite3.IntegrityError:
        st.error("Component code already exists.")
        return None
    except Error as e:
        st.error(f"Error adding component: {e}")
        return None


def get_trabajadores(conn):
    """Fetch all trabajadores from the users table"""
    sql = 'SELECT * FROM users'
    try:
        c = conn.cursor()
        c.execute(sql)
        trabajadores = c.fetchall()
        return trabajadores
    except Error as e:
        st.error(f"Error fetching trabajadores: {e}")
        return []
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

def add_entry(conn, worker_name, component_id, time_spent, date, quantity, start_time, end_time):
    """Add a new entry to the soldering_entries table without codification detail."""
    sql = '''INSERT INTO soldering_entries(worker_name, component_id, time_spent, date, quantity, start_time, end_time) VALUES(?,?,?,?,?,?,?)'''
    try:
        c = conn.cursor()
        c.execute(sql, (worker_name, component_id, time_spent, date, quantity, start_time, end_time))
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

def get_codifications_for_component(conn, component_id):
    """Fetch codifications for a given component"""
    sql = 'SELECT codification FROM component_codifications WHERE component_id = ?'
    try:
        c = conn.cursor()
        c.execute(sql, (component_id,))
        codifications = c.fetchall()
        return [cod[0] for cod in codifications]  # Devuelve solo las codificaciones como una lista de strings
    except Error as e:
        st.error(f"Error fetching codifications: {e}")
        return []

def add_codification(conn, component_id, codification):
    """Add a new codification for a component."""
    sql = 'INSERT INTO component_codifications(component_id, codification) VALUES(?, ?)'
    try:
        c = conn.cursor()
        c.execute(sql, (component_id, codification))
        conn.commit()
    except Error as e:
        st.error(f"Error adding codification: {e}")