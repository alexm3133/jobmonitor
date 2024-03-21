import pandas as pd
import sqlite3

def insert_employees_from_csv(csv_file_path, db_file_path):
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Crear la tabla de empleados si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            worker_name TEXT NOT NULL,
            worker_code INTEGER UNIQUE NOT NULL,
            worker_password TEXT NOT NULL,
            priority integer DEFAULT 2
        );
    ''')
    conn.commit()

    # Leer el archivo CSV
    df = pd.read_csv(csv_file_path, header=None, names=['worker_name', 'worker_code', 'worker_password', 'priority'])

    # Insertar empleados en la base de datos
    for index, row in df.iterrows():
        try:
            cursor.execute('''
                INSERT INTO users (worker_name, worker_code, worker_password, priority) 
                VALUES (?, ?, ?, ?)
            ''', (row['worker_name'], row['worker_code'], row['worker_password'], row['priority']))
        except sqlite3.IntegrityError as e:
            print(f"No se pudo insertar al empleado {row['worker_name']} debido a un error de integridad: {e}")
        except sqlite3.Error as e:
            print(f"Error al insertar al empleado {row['worker_name']}: {e}")
    
    # Guardar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

# Rutas a los archivos
csv_file_path = 'data/empleados.csv' 
db_file_path = 'soldering_db.sqlite'  

# Llamar a la función para insertar los empleados
insert_employees_from_csv(csv_file_path, db_file_path)
