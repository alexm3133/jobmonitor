import pandas as pd
import sqlite3

def insert_machines_from_csv(csv_file_path, db_file_path):
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    # Crear la tabla de máquinas si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY,
            machine_name TEXT UNIQUE NOT NULL
        );
    ''')
    conn.commit()

    # Leer el archivo CSV asumiendo que no tiene un encabezado y que la primera columna tiene los nombres de las máquinas
    df = pd.read_csv(csv_file_path, header=None, names=['machine_name'])

    # Insertar los nombres de las máquinas en la base de datos
    for machine_name in df['machine_name'].unique():
        try:
            cursor.execute('INSERT OR IGNORE INTO machines (machine_name) VALUES (?)', (machine_name,))
        except sqlite3.IntegrityError as e:
            print(f"No se pudo insertar la máquina {machine_name} debido a un error de integridad: {e}")
        except sqlite3.Error as e:
            print(f"Error al insertar la máquina {machine_name}: {e}")
    
    # Guardar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

# Ejemplo de cómo llamar a la función:
insert_machines_from_csv('data/maquinas.csv', 'soldering_db.sqlite')
