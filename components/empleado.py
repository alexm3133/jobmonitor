import streamlit as st
from database.repository import get_employee_data

def empleado(conn):
    """
    Displays a personalized employee space within the application.
    
    :param conn: The database connection object.
    """
    st.title('Tu espacio')

    # Verifica si 'user_id' está en st.session_state, de lo contrario muestra un error.
    if 'user_id' not in st.session_state:
        st.error("No estás autenticado. Por favor, inicia sesión.")
        return  # Finaliza la ejecución de la función si no hay user_id
    
    # Una vez confirmado que 'user_id' existe, procede a obtener los datos del empleado.
    user_id = st.session_state['user_id']
    employee_data = get_employee_data(conn, user_id)

    if employee_data:
        # Mostrando la información personal del empleado
        st.subheader("Información Personal")
        st.write(f"Nombre: {employee_data['name']}")
        st.write(f"Departamento: {employee_data['department']}")
    else:
        st.error("No se pudo cargar la información del empleado.")
