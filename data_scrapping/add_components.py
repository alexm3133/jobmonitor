
from sqlite3 import Error
import sqlite3

def add_patines_to_all_machines(db_file):
    conn = sqlite3.connect(db_file)
    if conn is not None:
        try:
            # Insert PATINES into the components table
            component_insert_query = "INSERT INTO components (component_name) VALUES ('PATINES') ON CONFLICT(component_name) DO NOTHING;"
            cur = conn.cursor()
            cur.execute(component_insert_query)
            conn.commit()

            # Retrieve the ID of PATINES
            cur.execute("SELECT id FROM components WHERE component_name = 'PATINES'")
            patines_id = cur.fetchone()[0]

            # Retrieve all machine IDs
            cur.execute("SELECT id FROM machines")
            machine_ids = cur.fetchall()

            # For each machine, create a relationship with PATINES in the machine_components table
            for machine_id in machine_ids:
                machine_component_insert_query = """
                INSERT INTO machine_components (machine_id, component_id)
                VALUES (?, ?)
                ON CONFLICT(machine_id, component_id) DO NOTHING;
                """
                cur.execute(machine_component_insert_query, (machine_id[0], patines_id))
                conn.commit()

            print("Component PATINES has been added to all machines.")
        except Error as e:
            print(f"Error during operation: {e}")
        finally:
            conn.close()
    else:
        print("Connection to database could not be established.")

# Example usage
db_file_path = 'soldering_db.sqlite'  
add_patines_to_all_machines(db_file_path)
