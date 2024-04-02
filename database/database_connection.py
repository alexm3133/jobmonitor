from sqlite3 import Error
import sqlite3

def create_connection(db_file):
    """
    Crea una conexión a la base de datos SQLite especificada por db_file.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Conexión establecida a {db_file}")
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return conn

def setup_database(conn):
    """
    Crea las tablas si no existen y realiza la configuración inicial necesaria.
    """
    sql_create_machines_table = """
    CREATE TABLE IF NOT EXISTS machines (
        id INTEGER PRIMARY KEY,
        machine_name TEXT NOT NULL
    );"""

    sql_create_components_table = """
    CREATE TABLE IF NOT EXISTS components (
        id INTEGER PRIMARY KEY,
        component_name TEXT NOT NULL
    );"""

    sql_create_machine_components_table = """
    CREATE TABLE IF NOT EXISTS machine_components (
        id INTEGER PRIMARY KEY,
        machine_id INTEGER NOT NULL,
        component_id INTEGER NOT NULL,
        FOREIGN KEY (machine_id) REFERENCES machines(id),
        FOREIGN KEY (component_id) REFERENCES components(id),
        UNIQUE (machine_id, component_id)
    );"""

    sql_create_component_codifications_table = """
    CREATE TABLE IF NOT EXISTS component_codifications (
        id INTEGER PRIMARY KEY,
        machine_id INTEGER NOT NULL,
        component_id INTEGER NOT NULL,
        codification TEXT NOT NULL,
        FOREIGN KEY (machine_id) REFERENCES machines(id),
        FOREIGN KEY (component_id) REFERENCES components(id),
        UNIQUE (machine_id, component_id, codification)
    );"""

    sql_create_soldering_entries_table = """
    CREATE TABLE IF NOT EXISTS soldering_entries (
        id INTEGER PRIMARY KEY,
        worker_name INTEGER NOT NULL,
        machine_id INTEGER NOT NULL,
        component_id INTEGER NOT NULL,
        codification_id INTEGER NOT NULL,
        time_spent REAL NOT NULL,
        date TEXT NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        observaciones TEXT,
        start_time TEXT,
        end_time TEXT,
        FOREIGN KEY (worker_name) REFERENCES users(id),
        FOREIGN KEY (machine_id) REFERENCES machines(id),
        FOREIGN KEY (component_id) REFERENCES components(id),
        FOREIGN KEY (codification_id) REFERENCES component_codifications(id)
    );"""

    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        worker_name TEXT NOT NULL,
        worker_code TEXT UNIQUE NOT NULL,
        worker_password TEXT NOT NULL,
        priority INTEGER DEFAULT 2
    );"""
    sql_create_events_table = """
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT,
        worker_id INTEGER,
        FOREIGN KEY (worker_id) REFERENCES users(id)
    );"""
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sql_create_machines_table)
            c.execute(sql_create_components_table)
            c.execute(sql_create_machine_components_table)
            c.execute(sql_create_component_codifications_table)
            c.execute(sql_create_soldering_entries_table)
            c.execute(sql_create_users_table)
            c.execute(sql_create_events_table)
            print("Las tablas de la base de datos han sido configuradas.")
        except Error as e:
            print(f"Error al crear las tablas: {e}")
    else:
        print("¡Error! No se pudo crear la conexión a la base de datos.")

# Ejemplo de uso
database = r"../soldering_db.sqlite"

conn = create_connection(database)

if conn is not None:
    setup_database(conn)
    conn.close()