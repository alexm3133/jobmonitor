import streamlit as st
from database.repository import add_trabajador

def administrar_trabajadores(conn):
    """
    Administra los trabajadores.

    Parameters:
    - conn: La conexión a la base de datos.

    Returns:
    None
    """
    st.header("Administrar Componentes")
    trabajador_name = st.text_input("Nombre del Trabajador", "")
    trabajador_code = st.text_input("Código del Trabajador", "")
    if st.button("Añadir Trabajador"):
        add_trabajador(conn, trabajador_name, trabajador_code)
        st.success("Trabajador añadido correctamente.")