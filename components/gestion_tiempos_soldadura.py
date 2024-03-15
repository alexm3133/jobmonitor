import streamlit as st  
from database.repository import add_entry, get_trabajadores, get_components, get_codifications_for_component
from datetime import datetime, time
from utils.calcular_horas_laborales import calcular_horas_laborales, segundos_a_horas_minutos
        
def gestion_tiempos_soldadura(conn):
    """
    Function to manage welding times.

    Parameters:
    - conn: The database connection object.

    Returns:
    None
    """
    st.title('Gestion Tiempos Soldadura')
    workers_name = get_trabajadores(conn)
    worker_options = {"Elija un empleado": None}
    worker_options.update({worker[1]: worker[0] for worker in workers_name})
    selected_worker = st.selectbox("Empleado", list(worker_options.keys()))
    selected_worker_id = worker_options[selected_worker]
    components = get_components(conn)
    component_options = {"Elija un componente": None}
    component_options.update({comp[1]: comp[0] for comp in components})
    selected_component = st.selectbox("Componente", list(component_options.keys()))
    selected_component_id = component_options[selected_component]
    if selected_component_id is not None:
        codifications = get_codifications_for_component(conn, selected_component_id)
    else:
        codifications = ["Elija una codificación"]
    selected_codification = st.selectbox("Codificación del Componente", codifications)
    quantity = st.number_input("Cantidad Soldada", min_value=1, value=1, step=1)
    start_date = st.date_input("Fecha de Inicio", datetime.now())
    end_date = st.date_input("Fecha de Fin", datetime.now())
    start_time = st.time_input("Hora de Inicio", time(6, 0))
    end_time = st.time_input("Hora de Fin", time(14, 0))
    start_datetime = datetime.combine(start_date, start_time).strftime("%Y-%m-%d %H:%M")
    end_datetime = datetime.combine(end_date, end_time).strftime("%Y-%m-%d %H:%M")
    if st.button("Añadir Entrada"):
        start_datetime = datetime.combine(start_date, start_time)
        end_datetime = datetime.combine(end_date, end_time)
        total_segundos = calcular_horas_laborales(start_datetime, end_datetime) * 3600
        horas_trabajadas, minutos_trabajados = segundos_a_horas_minutos(total_segundos)
        tiempo_trabajado_str = f"{int(horas_trabajadas)} horas y {int(minutos_trabajados)} minutos"
        tiempo_trabajado_decimal = horas_trabajadas + minutos_trabajados / 60.0
        add_entry(
            conn,
            selected_worker_id,
            selected_component_id,
            tiempo_trabajado_decimal,
            start_datetime.strftime("%Y-%m-%d %H:%M"),
            quantity,
            start_datetime.strftime("%Y-%m-%d %H:%M"),
            end_datetime.strftime("%Y-%m-%d %H:%M"),
            selected_codification
        )
        st.success(f"Entrada añadida correctamente! Tiempo trabajado: {tiempo_trabajado_str}")
