import streamlit as st
import pandas as pd
from datetime import datetime
from database.repository import get_workers, get_entries, get_machines, get_components, get_codifications_for_component, delete_entry
from sqlite3 import Error



def gestionar_entradas(conn):
    st.title('Historial de trabajo')

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

    # Obtener máquinas, componentes y codificaciones
    machines = {machine[0]: machine[1] for machine in get_machines(conn)}
    components = {}
    codifications = {}

    for machine_id, machine_name in machines.items():
        machine_components = get_components(conn, machine_id)
        for component_id, component_name in machine_components:
            components[(machine_id, component_id)] = (machine_name, component_name)
            codifications[(machine_id, component_id)] = get_codifications_for_component(conn, machine_id, component_id)

    # Crear DataFrame y realizar las uniones
    if entries:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM soldering_entries")
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(entries, columns=column_names)

        df['machine_name'] = df['machine_id'].map({machine_id: machine_name for machine_id, machine_name in machines.items()})
        df['component_name'] = df.apply(lambda row: components.get((row['machine_id'], row['component_id']), (None, None))[1], axis=1)
        df = df[['id','machine_name', 'component_name', 'codification_id', 'time_spent', 'quantity', 'start_time', 'end_time']]
        df = df.rename(columns={
            'id': 'ID',
            'machine_name': 'Maquina',
            'component_name': 'Componente',
            'codification_id': 'ID Codificación',
            'time_spent': 'Horas trabajadas',
            'quantity': 'Qt',
            'start_time': 'Fecha Inicio',
            'end_time': 'Fecha Fin'
        })

        st.dataframe(df)
    else:
        st.warning("No se encontraron entradas.")

    # Descargar CSV y preguntar donde guardarlo 

    if st.button("Descargar CSV"):
        csv = df.to_csv(index=False)
        st.download_button(label="Descargar CSV", data=csv, file_name="historial.csv", mime="text/csv")

    # Mostrar detalles de las entradas
    if st.checkbox("Mostrar detalles de las entradas"):
        st.write(entries)

    # borrar entradas y confirmar antes de borrar 
    if entries:
        entry_id = st.number_input("ID de la entrada a borrar", min_value=1, max_value=entries[-1][0], value=entries[-1][0], step=1)
        delete_clicked = st.button("Borrar entrada")
        if delete_clicked:
            delete_entry(conn, entry_id)
            st.success("Entrada borrada correctamente.")

