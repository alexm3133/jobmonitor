from streamlit_calendar import calendar as st_calendar
import streamlit as st
from database.repository import get_workers

def calendario(conn):
    # Sección lateral para mostrar la lista de trabajadores
    col1, col2 = st.columns([1, 4])
    with col1:
        st.write("Lista de Trabajadores")
        workers = get_workers(conn)
        worker_names = [worker[1] for worker in workers]  # Lista de nombres de trabajadores
        selected_worker = st.selectbox("Selecciona un trabajador", options=["Seleccione un trabajador"] + worker_names)
        if selected_worker != "Seleccione un trabajador":
            st.write(f"Trabajador seleccionado: {selected_worker}")
    with col2:
        # Obtener trabajadores
        workers = get_workers(conn)
        # Crear recursos de calendario para cada trabajador
        worker_resources = [{"id": str(worker[0]), "title": worker[1]} for worker in workers]
        
        calendar_options = {
            "editable": "true",
            "selectable": "true",
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridMonth,dayGridWeek,dayGridDay",
            },
            "initialView": "dayGridMonth",
            "resources": worker_resources,
        }
        
        custom_css="""
            .fc-event-past {
                opacity: 0.8;
            }
            .fc-event-time {
                font-style: italic;
            }
            .fc-event-title {
                font-weight: 700;
            }
            .fc-toolbar-title {
                font-size: 2rem;
            }
        """
        
        calendar_component = st_calendar(events=[], options=calendar_options, custom_css=custom_css)
        st.write(calendar_component)