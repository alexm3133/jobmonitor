import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection established to", db_file)
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def setup_database(conn):
    """Create tables if they do not exist and perform any necessary initial setup."""
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS components (
                                        id integer PRIMARY KEY,
                                        component_name text NOT NULL,
                                        component_code text UNIQUE NOT NULL
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS soldering_entries (
                                    id integer PRIMARY KEY,
                                    worker_name text NOT NULL,
                                    component_id integer NOT NULL,
                                    time_spent real NOT NULL,
                                    date text NOT NULL,
                                    codification text,
                                    quantity integer NOT NULL DEFAULT 1,
                                    start_time text,
                                    end_time text,
                                    FOREIGN KEY (component_id) REFERENCES components (id)
                                );"""

    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                    id integer PRIMARY KEY,
                                    trabajador_name text NOT NULL,
                                    trabajador_code text UNIQUE NOT NULL
                                );"""

    sql_create_codifications_table = """CREATE TABLE IF NOT EXISTS component_codifications (
                                            id integer PRIMARY KEY,
                                            component_id integer NOT NULL,
                                            codification text NOT NULL,
                                            FOREIGN KEY (component_id) REFERENCES components (id)
                                        );"""

    if conn is not None:
        # Create tables
        try:
            c = conn.cursor()
            c.execute(sql_create_projects_table)
            c.execute(sql_create_tasks_table)
            c.execute(sql_create_users_table)
            c.execute(sql_create_codifications_table)
            print("Database tables are set up.")
        except Error as e:
            print(f"Error creating tables: {e}")
    else:
        print("Error! cannot create the database connection.")

def main():
    database = "soldering_db.sqlite"

    # create a database connection
    conn = create_connection(database)

    # setup database tables
    setup_database(conn)

if __name__ == '__main__':
    main()
