import sqlite3
from sqlite3 import Error
import pandas as pd
import streamlit as st
import bcrypt

def add_worker(conn, worker_name, worker_code, worker_password, priority=2):
    """
    Añade un nuevo worker a la tabla de usuarios con contraseña hash.
    
    Parameters:
    - conn: La conexión a la base de datos.
    - worker_name: Nombre del worker.
    - worker_code: Código único del worker.
    - worker_password: Contraseña del worker.
    - priority: Prioridad del worker (1, 2, o 3).
    """
    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(worker_password.encode('utf-8'), bcrypt.gensalt())
    
    sql = '''INSERT INTO users(worker_name, worker_code, worker_password, priority)
             VALUES(?, ?, ?, ?)'''
    try:
        c = conn.cursor()
        c.execute(sql, (worker_name, worker_code, hashed_password, priority))
        conn.commit()
        st.success("Trabajador añadido correctamente.")
    except sqlite3.IntegrityError:
        st.error("El código del trabajador ya existe.")
    except Error as e:
        st.error(f"Error al añadir trabajador: {e}")

def add_machine(conn, machine_name):
    """Añade una nueva máquina a la tabla de máquinas."""
    sql = 'INSERT INTO machines(machine_name) VALUES(?)'
    try:
        c = conn.cursor()
        c.execute(sql, (machine_name,))
        conn.commit()
        return c.lastrowid
    except sqlite3.IntegrityError:
        st.error("El nombre de la máquina ya existe.")
        return None
    except Error as e:
        st.error(f"Error al añadir máquina: {e}")
        return None
def add_component(conn, component_name):
    """Añade un nuevo componente a la tabla de componentes."""
    sql = 'INSERT INTO components(component_name) VALUES(?)'
    try:
        c = conn.cursor()
        c.execute(sql, (component_name,))
        component_id = c.lastrowid
        conn.commit()
        return component_id
    except sqlite3.IntegrityError:
        st.error("El nombre del componente ya existe.")
        return None
    except Error as e:
        st.error(f"Error al añadir componente: {e}")
        return None

def add_machine_component(conn, machine_id, component_id):
    """Asocia un componente existente con una máquina."""
    sql = 'INSERT INTO machine_components(machine_id, component_id) VALUES(?, ?)'
    try:
        c = conn.cursor()
        c.execute(sql, (machine_id, component_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error("La combinación de máquina y componente ya existe.")
        return False
    except Error as e:
        st.error(f"Error al asociar componente con máquina: {e}")
        return False

def get_workers(conn):
    """Fetch all workers from the users table"""
    sql = 'SELECT * FROM users'
    try:
        c = conn.cursor()
        c.execute(sql)
        workers = c.fetchall()
        return workers
    except Error as e:
        st.error(f"Error fetching trabajadores: {e}")
        return []
def get_components(conn, machine_id=None):
    try:
        c = conn.cursor()
        if machine_id:
            sql = '''
                SELECT c.id, c.component_name
                FROM components c
                JOIN machine_components mc ON c.id = mc.component_id
                WHERE mc.machine_id = ?
            '''
            params = (machine_id,)
        else:
            sql = 'SELECT id, component_name FROM components'
            params = ()
        
        c.execute(sql, params)
        components = c.fetchall()
        return components
    except Error as e:
        st.error(f"Error fetching components: {e}")
        return []

def get_machines(conn):
    """Fetch all machines from the machines table."""
    sql = 'SELECT id, machine_name FROM machines'
    try:
        c = conn.cursor()
        c.execute(sql)
        machines = c.fetchall()
        return machines
    except Error as e:
        st.error(f"Error fetching machines: {e}")
        return []

def get_codifications_for_component(conn, machine_id, component_id):
    """Obtiene las codificaciones para un componente en una máquina específica."""
    sql = 'SELECT codification FROM component_codifications WHERE machine_id = ? AND component_id = ?'
    try:
        c = conn.cursor()
        c.execute(sql, (machine_id, component_id))
        codifications = c.fetchall()
        return [cod[0] for cod in codifications]  # Devuelve solo las codificaciones como una lista de strings
    except Error as e:
        st.error(f"Error fetching codifications: {e}")
        return []
def add_codification(conn, machine_id, component_id, codification):
    """Añade una nueva codificación para un componente en una máquina específica."""
    sql = 'INSERT INTO component_codifications(machine_id, component_id, codification) VALUES(?, ?, ?)'
    try:
        c = conn.cursor()
        c.execute(sql, (machine_id, component_id, codification))
        conn.commit()
        return True  # Indica éxito
    except Error as e:
        st.error(f"Error añadiendo codificación al componente: {e}")
        return False  # Indica fallo
    
def get_codification_id(conn, machine_id, component_id, codification):
    """Obtiene el ID de la codificación para una combinación de máquina, componente y codificación."""
    sql = 'SELECT id FROM component_codifications WHERE machine_id = ? AND component_id = ? AND codification = ?'
    try:
        c = conn.cursor()
        c.execute(sql, (machine_id, component_id, codification))
        codification_id = c.fetchone()
        return codification_id[0] if codification_id else None
    except Error as e:
        st.error(f"Error obteniendo el ID de la codificación: {e}")
        return None

def add_entry(conn, worker_name, machine_id, component_id, codification_id, time_spent, start_datetime, quantity, observaciones, start_datetime_str, end_datetime_str):
    """Añade una nueva entrada a la tabla soldering_entries con el detalle de tiempo y codificación."""
    sql = '''INSERT INTO soldering_entries(worker_name, machine_id, component_id, codification_id, time_spent, date, quantity, observaciones, start_time, end_time) VALUES(?,?,?,?,?,?,?,?,?,?)'''
    date = start_datetime.split(' ')[0]
    try:
        c = conn.cursor()
        c.execute(sql, (worker_name, machine_id, component_id, codification_id, time_spent, date, quantity, observaciones, start_datetime_str, end_datetime_str))
        conn.commit()
        st.success("Entrada añadida correctamente.")
    except Error as e:
        st.error(f"Error al añadir entrada: {e}")

def get_entries(conn, worker_name=None,observaciones=None, start_date=None, end_date=None):
    """Fetch soldering entries from the soldering_entries table."""
    conditions = []
    params = []

    if worker_name:
        conditions.append("worker_name = ?")
        params.append(worker_name)
    
    #get observaciones
    if observaciones:
        conditions.append("observaciones = ?")
        params.append(observaciones)

    if start_date and end_date:
        conditions.append("date BETWEEN ? AND ?")
        params.extend([start_date, end_date])
    elif start_date:
        conditions.append("date >= ?")
        params.append(start_date)
    elif end_date:
        conditions.append("date <= ?")
        params.append(end_date)

    where_clause = " AND ".join(conditions) if conditions else ""
    sql = f"SELECT * FROM soldering_entries WHERE {where_clause}"

    try:
        c = conn.cursor()
        c.execute(sql, params)
        entries = c.fetchall()
        return entries
    except Error as e:
        st.error(f"Error fetching entries: {e}")
        return []
    
def add_machine_component(conn, machine_id, component_id):
    """Asocia un componente existente con una máquina."""
    sql = 'INSERT INTO machine_components(machine_id, component_id) VALUES(?, ?)'
    try:
        c = conn.cursor()
        c.execute(sql, (machine_id, component_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error("La combinación de máquina y componente ya existe.")
        return False
    except Error as e:
        st.error(f"Error al asociar componente con máquina: {e}")
        return False
    
def verificar_solapamiento(conn, worker_id, start_datetime, end_datetime):
    """Verifica si hay solapamiento de horario para el mismo trabajador."""
    sql = '''
    SELECT COUNT(*) FROM soldering_entries
    WHERE worker_name = ? AND (
        (start_time BETWEEN ? AND ?)
        OR (end_time BETWEEN ? AND ?)
        OR (start_time <= ? AND end_time >= ?)
    )
    '''
    try:
        c = conn.cursor()
        c.execute(sql, (worker_id, start_datetime, end_datetime, start_datetime, end_datetime, start_datetime, end_datetime))
        result = c.fetchone()
        if result[0] > 0:
            # Existe solapamiento
            return True
        return False
    except Error as e:
        st.error(f"Error verificando solapamiento: {e}")
        return True  # Por defecto, asumir que hay un error/solapamiento para evitar añadir entradas conflictivas.

def component_exists_in_machine(conn, machine_id, component_name):
    components = get_components(conn, machine_id)
    return any(comp[1] == component_name for comp in components)

def delete_entry(conn, entry_id):
    """
    Borra una entrada específica de la tabla soldering_entries basándose en su id.
    
    Parameters:
    - conn: La conexión a la base de datos.
    - entry_id: El identificador único de la entrada a borrar.
    """
    sql = "DELETE FROM soldering_entries WHERE id = ?"
    try:
        c = conn.cursor()
        c.execute(sql, (entry_id,))
        conn.commit()
        st.success("Entrada borrada correctamente.")
    except Error as e:
        st.error(f"Error al borrar la entrada: {e}")

def get_employee_data(conn, user_id):
    """
    Obtiene los datos de un empleado específico de la tabla de usuarios.
    
    Parameters:
    - conn: La conexión a la base de datos.
    - user_id: El identificador único del empleado.
    
    Returns:
    Una tupla con los datos del empleado o None si el empleado no existe.
    """
    sql = 'SELECT * FROM users WHERE worker_code = ?'
    try:
        c = conn.cursor()
        c.execute(sql, (user_id,))
        employee_data = c.fetchone()
        if employee_data:
            # Suponiendo que la tabla 'users' tiene las columnas 'id', 'worker_name', 'worker_code', 'worker_password', y 'priority'
            # Convertir la tupla a un diccionario para un manejo más fácil de los datos
            columns = ['id', 'worker_name', 'worker_code', 'worker_password', 'priority']
            return dict(zip(columns, employee_data))
        else:
            return None
    except Error as e:
        st.error(f"Error al obtener los datos del empleado: {e}")
        return None

def add_event(conn, title, start_date, end_date, worker_id=None):
    sql = '''INSERT INTO events(title, start_date, end_date, worker_id)
             VALUES(?, ?, ?, ?)'''
    c = conn.cursor()
    c.execute(sql, (title, start_date, end_date, worker_id))
    conn.commit()

def get_events(conn, worker_id=None):
    sql = '''
    SELECT e.id, e.title, e.start_date, e.end_date, e.worker_id, u.worker_name
    FROM events e
    LEFT JOIN users u ON e.worker_id = u.id
    '''
    if worker_id:
        sql += ' WHERE e.worker_id = ?'
        params = (worker_id,)
    else:
        params = ()
    c = conn.cursor()
    c.execute(sql, params)
    return c.fetchall()


def delete_event(conn, event_id):
    """
    Elimina un evento específico por su ID.
    """
    sql = 'DELETE FROM events WHERE id = ?'
    try:
        c = conn.cursor()
        c.execute(sql, (event_id,))
        conn.commit()
    except Error as e:
        print(f"Error al eliminar el evento: {e}")
