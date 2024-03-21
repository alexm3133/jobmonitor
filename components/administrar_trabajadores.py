import streamlit as st
from database.repository import add_worker

def administrar_workers(conn):
    """
    Administra los trabajadores, permitiendo añadir nuevos con nombre, código y contraseña.

    Parameters:
    - conn: La conexión a la base de datos.
    """
    st.header("Administrar Trabajadores")
    worker_name = st.text_input("Nombre del Trabajador", "")
    worker_code = st.text_input("Código del Trabajador", "")
    worker_password = st.text_input("Contraseña del Trabajador", type="password")
    priority = st.selectbox("Prioridad del Trabajador", [1, 2, 3], index=1)
    if st.button("Añadir Trabajador"):
        add_worker(conn, worker_name, worker_code, worker_password, priority)
