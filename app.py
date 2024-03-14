from datetime import datetime, timedelta, time
import streamlit as st
from database.database import create_connection, add_component, get_components, add_entry, get_entries, delete_entry, generate_report, add_trabajador, get_trabajadores, get_codifications_for_component, add_codification 
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

database = "soldering_db.sqlite"
conn = create_connection(database)

menu_options = ["Gestion Tiempos Soldadura", "Gestionar entradas", "Generar Reporte", "Administrar Componentes", "Administrar Trabajadores"]
selected_option = st.sidebar.selectbox("Menú", menu_options)

if selected_option == "Gestion Tiempos Soldadura":
    st.title('Gestion Tiempos Soldadura')
    # Obtener nombres y IDs de trabajadores y componentes
    workers_name = get_trabajadores(conn)
    worker_options = {worker[1]: worker[0] for worker in workers_name}
    selected_worker = st.selectbox("Empleado", list(worker_options.keys()))
    selected_worker_id = worker_options[selected_worker]
    
    components = get_components(conn)
    component_options = {comp[1]: comp[0] for comp in components}  
    selected_component = st.selectbox("Componente", list(component_options.keys()))
    selected_component_id = component_options[selected_component]
    
    # Entradas para codificación y cantidad
    codifications = get_codifications_for_component(conn, selected_component_id)
    selected_codification = st.selectbox("Codificación del Componente", codifications)
    quantity = st.number_input("Cantidad Soldada", min_value=1, value=1, step=1)
    
    # Entradas para fechas de inicio y fin, y duración en minutos
    start_date = st.date_input("Fecha de Inicio", datetime.now())
    end_date = st.date_input("Fecha de Fin", datetime.now())
    duration_minutes = st.number_input("Duración (minutos)", min_value=0, value=0, step=1)

    # Convertir la duración a horas para mantener la consistencia con la base de datos
    time_spent_hours = duration_minutes / 60
    
    if st.button("Añadir Entrada"):
        # Llama a add_entry sin el argumento 'selected_codification'
        add_entry(conn, selected_worker_id, selected_component_id, time_spent_hours, start_date.strftime("%Y-%m-%d"), quantity, start_date.strftime("%H:%M"), end_date.strftime("%H:%M"))
        st.success("Entrada añadida correctamente!")


elif selected_option == "Gestionar entradas":
    st.header("Gestionar entradas")
    entries = get_entries(conn)
    entries_df = pd.DataFrame(entries, columns=['ID', 'Date', 'Time Spent', 'Component Name', 'Component Code', 'Worker Name'])
    st.dataframe(entries_df)
    entry_id_to_edit_or_delete = st.number_input("Enter ID of entry to edit or delete", min_value=0, format="%d", key="edit_delete")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete", key="delete"):
            delete_entry(conn, entry_id_to_edit_or_delete)
            st.success(f"Entry {entry_id_to_edit_or_delete} deleted successfully!")
    with col2:
        if st.button("Edit", key="edit"):
            pass
elif selected_option == "Generar Reporte":
    st.header("Generar Reporte")
    start_date = st.date_input("Fecha de Inicio", datetime.now() - timedelta(days=30))
    end_date = st.date_input("Fecha de Fin", datetime.now())

    # Permitir al usuario seleccionar un componente específico
    component_names = [comp[1] for comp in get_components(conn)]  # Asume que get_components retorna una lista de tuplas (id, nombre)
    selected_component_name = st.selectbox("Selecciona el componente:", component_names)
    
    if st.button("Generar"):
        report_df = generate_report(conn, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        
        # Filtrar el reporte por el componente seleccionado
        filtered_df = report_df[report_df['Component Name'] == selected_component_name]
        
        if not filtered_df.empty:
            import plotly.express as px

            # Agrupa por 'Worker Name' y calcula el tiempo total gastado en el componente seleccionado
            grouped_df = filtered_df.groupby(['Worker Name'])['Time Spent'].sum().reset_index()

            # Dibujar un gráfico de barras con Plotly
            fig = px.bar(grouped_df, x='Worker Name', y='Time Spent',
                         title=f'Tiempo Total Gastado por Trabajador en {selected_component_name}',
                         labels={'Time Spent': 'Tiempo Gastado (horas)', 'Worker Name': 'Trabajador'},
                         color='Time Spent',  # Esto asignará colores basados en el tiempo gastado
                         color_continuous_scale=px.colors.sequential.Viridis)  # Usa una escala de colores predefinida

            # Mejora de la estilización
            fig.update_layout(
                xaxis_title="Trabajador",
                yaxis_title="Tiempo Gastado (horas)",
                plot_bgcolor='rgba(0,0,0,0)',  # Fondo transparente
                xaxis_tickangle=-45,  # Ángulo de las etiquetas del eje x
                template='plotly_white',  # Utiliza el tema 'plotly_white' para un fondo claro
            )

            st.plotly_chart(fig)

        else:
            st.write("No hay datos disponibles para el componente seleccionado en el rango de fechas dado.")


elif selected_option == "Administrar Componentes":
    st.header("Administrar Componentes")
    component_name = st.text_input("Nombre del Componente", "")

    codification_text = st.text_input("Codificación del Componente", "")  

    if st.button("Añadir Componente"):
        component_id = add_component(conn, component_name, codification_text)
        if component_id:
            add_codification(conn, component_id, codification_text)
            st.success("Componente y codificación añadidos correctamente.")


        
elif selected_option == "Administrar Trabajadores":
    st.header("Administrar Componentes")
    trabajador_name = st.text_input("Nombre del Trabajador", "")
    trabajador_code = st.text_input("Código del Trabajador", "")
    if st.button("Añadir Trabajador"):
        add_trabajador(conn,trabajador_name, trabajador_code)
        st.success("Trabajador añadido correctamente.")

