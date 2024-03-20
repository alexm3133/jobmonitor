import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """
    Create a database connection to the SQLite database specified by db_file.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection established to", db_file)
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def setup_database(conn):
    """
    Create tables if they do not exist and perform any necessary initial setup.
    """
    # Nueva tabla para Máquinas
    sql_create_machines_table = """
    CREATE TABLE IF NOT EXISTS machines (
        id integer PRIMARY KEY,
        machine_name text UNIQUE NOT NULL
    ); """

    # Modificar la tabla de Componentes para incluir machine_id
    sql_create_components_table = """
    CREATE TABLE IF NOT EXISTS components (
        id integer PRIMARY KEY,
        machine_id integer NOT NULL,
        component_name text UNIQUE NOT NULL,
        FOREIGN KEY (machine_id) REFERENCES machines(id)
    ); """
    
    sql_create_soldering_entries_table = """
    CREATE TABLE IF NOT EXISTS soldering_entries (
        id integer PRIMARY KEY,
        worker_id integer NOT NULL,  -- Cambiado de worker_name a worker_id para usar el ID del trabajador
        machine_id integer NOT NULL,
        component_id integer NOT NULL,
        time_spent real NOT NULL,
        date text NOT NULL,
        codification text,
        quantity integer NOT NULL DEFAULT 1,
        start_time text,
        end_time text,
        FOREIGN KEY (worker_id) REFERENCES users (id),  -- Asegúrate de que la clave foránea ahora apunta correctamente a users
        FOREIGN KEY (machine_id) REFERENCES machines (id),
        FOREIGN KEY (component_id) REFERENCES components (id)
    );"""

    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY,
        trabajador_name text NOT NULL,
        trabajador_code text UNIQUE NOT NULL,
        trabajador_password text NOT NULL,
        priority integer DEFAULT 2
    );"""

    sql_create_codifications_table = """
    CREATE TABLE IF NOT EXISTS component_codifications (
        id integer PRIMARY KEY,
        component_id integer NOT NULL,
        codification text NOT NULL,
        UNIQUE(component_id, codification),
        FOREIGN KEY (component_id) REFERENCES components (id)
    );"""

    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sql_create_components_table)
            c.execute(sql_create_machines_table)
            c.execute(sql_create_soldering_entries_table)
            c.execute(sql_create_users_table)
            c.execute(sql_create_codifications_table)
            print("Database tables are set up.")
            
        except Error as e:
            print(f"Error creating tables: {e}")
    else:
        print("Error! cannot create the database connection.")

