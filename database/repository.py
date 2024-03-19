import sqlite3
from sqlite3 import Error
import pandas as pd
import streamlit as st

def add_trabajador(conn, trabajador_name, trabajador_code, trabajador_password):
    """
    Añade un nuevo trabajador a la tabla de usuarios con contraseña.

    Parameters:
    - conn: La conexión a la base de datos.
    - trabajador_name: Nombre del trabajador.
    - trabajador_code: Código único del trabajador.
    - trabajador_password: Contraseña del trabajador.
    """
    sql = '''INSERT INTO users(trabajador_name, trabajador_code, trabajador_password)
             VALUES(?, ?, ?)'''
    try:
        c = conn.cursor()
        c.execute(sql, (trabajador_name, trabajador_code, trabajador_password))
        conn.commit()
        st.success("Trabajador añadido correctamente.")
    except sqlite3.IntegrityError:
        st.error("El código del trabajador ya existe.")
    except Error as e:
        st.error(f"Error al añadir trabajador: {e}")
def add_component(conn, component_name):
    """Add a new component to the components table and return its ID."""
    sql = 'INSERT INTO components(component_name) VALUES(?)'
    try:
        c = conn.cursor()
        c.execute(sql, (component_name,))
        conn.commit()
        return c.lastrowid  # Devuelve el ID del nuevo componente
    except sqlite3.IntegrityError:
        st.error("Component name already exists.")
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
    
def add_entry(conn, worker_name, component_id, time_spent, start_datetime, quantity, start_datetime_str, end_datetime_str, codification):
    """Add a new entry to the soldering_entries table with detailed time and codification."""
    sql = '''INSERT INTO soldering_entries(worker_name, component_id, time_spent, date, quantity, start_time, end_time, codification) VALUES(?,?,?,?,?,?,?,?)'''
    # La fecha ahora se extrae del 'start_datetime'
    date = start_datetime.split(' ')[0]
    try:
        c = conn.cursor()
        # Asegúrate de pasar los argumentos en el orden correcto y formatear las fechas/horas como strings si es necesario
        c.execute(sql, (worker_name, component_id, time_spent, date, quantity, start_datetime_str, end_datetime_str, codification))
        conn.commit()
    except Error as e:
        st.error(f"Error adding entry: {e}")


def get_entries(conn):
    """Fetch entries with component, piece, codification, worker, start/end dates, quantity, and calculate total and average time spent per piece."""
    sql = '''
    SELECT 
        c.component_name, 
        se.codification, 
        u.trabajador_name, 
        se.start_time AS 'Start Date', 
        se.end_time AS 'End Date', 
        se.quantity AS 'Quantity', 
        se.time_spent AS 'Total Time Spent',
        (se.time_spent / se.quantity) AS 'Average Time Per Piece'
    FROM soldering_entries se
    JOIN components c ON se.component_id = c.id
    JOIN users u ON se.worker_name = u.id
    '''
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
    """Generate a report of entries within a specific date range, including worker names."""
    sql = '''
    SELECT se.date, se.time_spent, c.component_name, c.component_code, u.trabajador_name 
    FROM soldering_entries se
    JOIN components c ON se.component_id = c.id
    JOIN users u ON u.id = se.worker_name  -- Asegúrate de que esta sea la relación correcta
    WHERE se.date BETWEEN ? AND ?
    '''
    try:
        c = conn.cursor()
        c.execute(sql, (start_date, end_date))
        entries = c.fetchall()
        # Asegúrate de que las columnas se mapean correctamente a los nombres en tu DataFrame
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
