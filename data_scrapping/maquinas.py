import pandas as pd
import sqlite3

def insert_machines_from_csv(csv_file_path, db_file_path):

    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY,
            machine_name TEXT UNIQUE NOT NULL
        );
    ''')
    conn.commit()

    df = pd.read_csv(csv_file_path, header=None, names=['machine_name'])

    for machine_name in df['machine_name'].unique():
        try:
            cursor.execute('INSERT OR IGNORE INTO machines (machine_name) VALUES (?)', (machine_name,))
        except sqlite3.IntegrityError as e:
            print(f"No se pudo insertar la máquina {machine_name} debido a un error de integridad: {e}")
        except sqlite3.Error as e:
            print(f"Error al insertar la máquina {machine_name}: {e}")
    
    conn.commit()
    conn.close()

insert_machines_from_csv('data/maquinas.csv', 'soldering_db.sqlite')
