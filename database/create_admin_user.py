import sqlite3
import bcrypt

def create_admin_user(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear la tabla de usuarios si no existe
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        worker_name TEXT NOT NULL,
        worker_code TEXT UNIQUE NOT NULL,
        worker_password TEXT NOT NULL,
        priority INTEGER DEFAULT 2
    );"""
    cursor.execute(sql_create_users_table)

    # Verificar si el usuario administrador ya existe usando worker_code
    cursor.execute("SELECT * FROM users WHERE worker_code = 'admin'")
    if cursor.fetchone() is None:
        # Si no existe, crear el usuario administrador
        password = "test"
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        try:
            cursor.execute("INSERT INTO users (worker_name, worker_code, worker_password, priority) VALUES (?, ?, ?, ?)",
                           ('Admin', 'admin', password_hash, 1))
            conn.commit()
            print("Administrador creado con éxito.")
        except sqlite3.IntegrityError:
            print("Error: El código de trabajador 'admin' ya está en uso.")
    else:
        print("El usuario administrador ya existe.")

    conn.close()
