import streamlit as st
from database.repository import add_trabajador

def administrar_trabajadores(conn):
    """
    Administra los trabajadores, permitiendo añadir nuevos con nombre, código y contraseña.

    Parameters:
    - conn: La conexión a la base de datos.
    """
    st.header("Administrar Trabajadores")
    trabajador_name = st.text_input("Nombre del Trabajador", "")
    trabajador_code = st.text_input("Código del Trabajador", "")
    trabajador_password = st.text_input("Contraseña del Trabajador", type="password")
    priority = st.selectbox("Prioridad del Trabajador", [1, 2, 3], index=1)
    if st.button("Añadir Trabajador"):
        add_trabajador(conn, trabajador_name, trabajador_code, trabajador_password, priority)
