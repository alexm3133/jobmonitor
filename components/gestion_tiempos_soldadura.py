import streamlit as st  
from database.repository import add_entry, get_trabajadores, get_components, get_codifications_for_component, get_machines
from datetime import datetime, time
from utils.calcular_horas_laborales import calcular_horas_laborales, segundos_a_horas_minutos
        
def gestion_tiempos_soldadura(conn):
    st.title('Gestion Tiempos Soldadura')
    
    # Obtener trabajadores
    workers_name = get_trabajadores(conn)
    worker_options = {"Elija un empleado": None}
    worker_options.update({worker[1]: worker[0] for worker in workers_name})
    selected_worker = st.selectbox("Empleado", list(worker_options.keys()))
    selected_worker_id = worker_options[selected_worker]

    # Obtener máquinas
    machines = get_machines(conn)
    machine_options = {"Elija una máquina": None}
    machine_options.update({machine[1]: machine[0] for machine in machines})
    selected_machine = st.selectbox("Máquina", list(machine_options.keys()))
    selected_machine_id = machine_options[selected_machine]

    # Obtener componentes basados en la máquina seleccionada
    if selected_machine_id:
        components = get_components(conn, selected_machine_id)  # Asume que get_components ahora acepta machine_id
    else:
        components = []
    component_options = {"Elija un componente": None}
    component_options.update({comp[1]: comp[0] for comp in components})
    selected_component = st.selectbox("Componente", list(component_options.keys()))
    selected_component_id = component_options[selected_component]

    # Obtener codificaciones para el componente seleccionado
    codifications = get_codifications_for_component(conn, selected_component_id) if selected_component_id else ["Elija una codificación"]
    selected_codification = st.selectbox("Codificación del Componente", codifications)

    # Otras entradas del formulario
    quantity = st.number_input("Cantidad Soldada", min_value=1, value=1, step=1)
    start_date = st.date_input("Fecha de Inicio", datetime.now())
    end_date = st.date_input("Fecha de Fin", datetime.now())
    start_time = st.time_input("Hora de Inicio", time(6, 30))
    end_time = st.time_input("Hora de Fin", time(14, 30))
    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(end_date, end_time)

    # Añadir entrada
    if st.button("Añadir Entrada"):
        total_segundos = calcular_horas_laborales(start_datetime, end_datetime) * 3600
        horas_trabajadas, minutos_trabajados = segundos_a_horas_minutos(total_segundos)
        tiempo_trabajado_decimal = horas_trabajadas + minutos_trabajados / 60
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
        st.success(f"Entrada añadida correctamente! Tiempo trabajado: {horas_trabajadas} horas y {minutos_trabajados} minutos")
