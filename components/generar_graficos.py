from datetime import datetime, timedelta, time
import streamlit as st
from database.repository import get_components, generate_report

def generar_graficos(conn):
    st.header("Generar Reporte")
    start_date = st.date_input("Fecha de Inicio", datetime.now() - timedelta(days=30))
    end_date = st.date_input("Fecha de Fin", datetime.now())
    start_time = st.time_input("Hora de Inicio", time(6, 0))  # Ejemplo: comienza a las 9:00 por defecto
    end_time = st.time_input("Hora de Fin", time(14, 0))  # Ejemplo: termina a las 17:00 por defecto
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