from streamlit_calendar import calendar as st_calendar
import streamlit as st
from database.repository import get_workers, add_event, get_events, delete_event

def calendario(conn):
    # Sección lateral para mostrar la lista de trabajadores
    col1, col2 = st.columns([1, 4])
    with col1:
        st.write("Lista de Trabajadores")
        workers = get_workers(conn)
        worker_names = [worker[1] for worker in workers]  # Lista de nombres de trabajadores
        worker_ids = {worker[1]: worker[0] for worker in workers}  # Diccionario de nombre: id
        all_workers_option = "Todos los trabajadores"
        worker_selection_options = [all_workers_option] + worker_names
        selected_worker_name = st.selectbox("Selecciona un trabajador", options=worker_selection_options)
        selected_worker_id = worker_ids.get(selected_worker_name) if selected_worker_name != all_workers_option else None

    # Añadir eventos
    with col2:
        if selected_worker_name != all_workers_option:
            st.write("Añadir Evento")
            with st.form("event_form"):
                title = st.text_input("Título del Evento")
                start_date = st.date_input("Fecha de Inicio")
                submit_button = st.form_submit_button("Añadir Evento")
                
                if submit_button:
                    add_event(conn, title, start_date, None, selected_worker_id)
                    st.success("Evento añadido")

        # Mostrar eventos en el calendario para el trabajador seleccionado o todos
        if selected_worker_id:
            events = get_events(conn, selected_worker_id)
        else:
            events = get_events(conn)  # Llama a get_events sin parámetros para obtener todos los eventos

        events_for_calendar = [{"title": event[1], "start": event[2], "end": event[3] if event[3] else event[2], "resourceId": event[0]} for event in events]

        calendar_options = {
            "editable": "true",
            "selectable": "true",
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridMonth,dayGridWeek,dayGridDay",
            },
            "initialView": "dayGridMonth",
            "events": events_for_calendar
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

        calendar_component = st_calendar(options=calendar_options, custom_css=custom_css)
        st.write(calendar_component)

        st.write("Eliminar Evento")
        if selected_worker_id:
            events = get_events(conn, selected_worker_id)
        else:
            events = get_events(conn)

        if events:
            event_titles = {f"{event[1]} ({event[2]} - {event[3]})": event[0] for event in events}  # crea un diccionario título: id
            selected_event_to_delete = st.selectbox("Selecciona un evento para eliminar", options=[""] + list(event_titles.keys()))
            if st.button("Eliminar Evento Seleccionado"):
                if selected_event_to_delete:  # asegúrate de que se haya seleccionado un evento
                    delete_event(conn, event_titles[selected_event_to_delete])
                    st.success("Evento eliminado correctamente")
                else:
                    st.error("Por favor, selecciona un evento para eliminar")
        else:
            st.write("No hay eventos para mostrar")
