import streamlit as st  
from database.repository import add_entry, get_trabajadores, get_components, get_codifications_for_component
from datetime import datetime, time
from utils.calcular_horas_laborales import calcular_horas_laborales, segundos_a_horas_minutos
        
def gestion_tiempos_soldadura(conn):        
        st.title('Gestion Tiempos Soldadura')
        # Obtener nombres y IDs de trabajadores y componentes
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
        
        # Asegurarse de que un componente ha sido seleccionado antes de intentar obtener codificaciones
        if selected_component_id is not None:
            codifications = get_codifications_for_component(conn, selected_component_id)
        else:
            codifications = ["Elija una codificación"]
        selected_codification = st.selectbox("Codificación del Componente", codifications)
        
        # Entradas para cantidad, establecer 0 o None como valor predeterminado si deseas que el usuario explícitamente ingrese un valor
        quantity = st.number_input("Cantidad Soldada", min_value=1, value=1, step=1)

        # Entradas para fechas de inicio y fin, y duración en minutos
        start_date = st.date_input("Fecha de Inicio", datetime.now())
        end_date = st.date_input("Fecha de Fin", datetime.now())
        start_time = st.time_input("Hora de Inicio", time(6, 0))  
        end_time = st.time_input("Hora de Fin", time(14, 0)) 
        start_datetime = datetime.combine(start_date, start_time).strftime("%Y-%m-%d %H:%M")
        end_datetime = datetime.combine(end_date, end_time).strftime("%Y-%m-%d %H:%M")

        if st.button("Añadir Entrada"):
            start_datetime = datetime.combine(start_date, start_time)
            end_datetime = datetime.combine(end_date, end_time)
            total_segundos = calcular_horas_laborales(start_datetime, end_datetime) * 3600  # Convertir horas a segundos
            horas_trabajadas, minutos_trabajados = segundos_a_horas_minutos(total_segundos)
            
            # Formatear la salida para incluir tanto horas como minutos
            tiempo_trabajado_str = f"{int(horas_trabajadas)} horas y {int(minutos_trabajados)} minutos"
            
            # A continuación, puedes usar 'tiempo_trabajado_str' para mostrarlo en la UI
            # O convertir 'horas_trabajadas' y 'minutos_trabajados' a un decimal o a la forma que prefieras para almacenar en la base de datos
            # Por ejemplo, si prefieres almacenar en horas como decimal:
            tiempo_trabajado_decimal = horas_trabajadas + minutos_trabajados / 60.0
            
            # Luego procedes a añadir la entrada con el tiempo trabajado
            add_entry(conn, selected_worker_id, selected_component_id, tiempo_trabajado_decimal, start_datetime.strftime("%Y-%m-%d %H:%M"), quantity, start_datetime.strftime("%Y-%m-%d %H:%M"), end_datetime.strftime("%Y-%m-%d %H:%M"), selected_codification)
            st.success(f"Entrada añadida correctamente! Tiempo trabajado: {tiempo_trabajado_str}")
