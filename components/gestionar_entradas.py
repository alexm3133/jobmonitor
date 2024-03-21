import streamlit as st
import pandas as pd
from datetime import datetime
from database.repository import get_workers, get_entries, get_machines, get_components

def gestionar_entradas(conn):
    st.title('Gestionar Entradas')

    # Obtener trabajadores
    workers = get_workers(conn)
    worker_options = {worker[1]: worker[0] for worker in workers}
    worker_options['Todos los trabajadores'] = None

    # Filtrar por trabajador
    selected_worker = st.selectbox("Empleado", list(worker_options.keys()))
    selected_worker_name = worker_options.get(selected_worker)

    # Filtrar por fechas
    start_date = st.date_input("Fecha de Inicio", value=datetime.now(), key="start_date")
    end_date = st.date_input("Fecha de Fin", value=datetime.now(), key="end_date")

    # Obtener entradas
    entries = get_entries(conn, worker_name=selected_worker_name, start_date=start_date, end_date=end_date)

    # Obtener máquinas y componentes
    machines = {machine[0]: machine[1] for machine in get_machines(conn)}
    components = {component[0]: component[1] for component in get_components(conn)}

    # Crear DataFrame y realizar las uniones
    if entries:
        # Get column names from the description of the cursor
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM soldering_entries")
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(entries, columns=column_names)
        df['machine_name'] = df['machine_id'].map(machines)
        df['component_name'] = df['component_id'].map(components)
        df = df[['machine_name', 'component_name', 'time_spent', 'date', 'quantity', 'start_time', 'end_time']]
        st.dataframe(df)
    else:
        st.warning("No se encontraron entradas.")