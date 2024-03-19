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
            trabajador_name TEXT NOT NULL,
            trabajador_code INTEGER UNIQUE NOT NULL,
            trabajador_password TEXT NOT NULL
        );
    ''')
    conn.commit()

    # Leer el archivo CSV
    df = pd.read_csv(csv_file_path, header=None, names=['trabajador_name', 'trabajador_code', 'trabajador_password'])

    # Insertar empleados en la base de datos
    for index, row in df.iterrows():
        try:
            cursor.execute('''
                INSERT INTO users (trabajador_name, trabajador_code, trabajador_password) 
                VALUES (?, ?, ?)
            ''', (row['trabajador_name'], row['trabajador_code'], row['trabajador_password']))
        except sqlite3.IntegrityError as e:
            print(f"No se pudo insertar al empleado {row['trabajador_name']} debido a un error de integridad: {e}")
        except sqlite3.Error as e:
            print(f"Error al insertar al empleado {row['trabajador_name']}: {e}")
    
    # Guardar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

# Rutas a los archivos
csv_file_path = 'data/empleados.csv' 
db_file_path = 'soldering_db.sqlite'  

# Llamar a la función para insertar los empleados
insert_employees_from_csv(csv_file_path, db_file_path)
