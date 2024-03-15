from datetime import datetime, timedelta
import streamlit as st
from database.repository import get_components, generate_report
import plotly.express as px

def generar_graficos(conn):
    """
    Generates a report with a bar chart showing the total time spent by each worker on a selected component.

    Parameters:
    - conn: The database connection object.

    Returns:
    None
    """
    st.header("Generar Reporte")
    start_date = st.date_input("Fecha de Inicio", datetime.now() - timedelta(days=30))
    end_date = st.date_input("Fecha de Fin", datetime.now())
    component_names = [comp[1] for comp in get_components(conn)]  
    selected_component_name = st.selectbox("Selecciona el componente:", component_names)
    if st.button("Generar"):
        report_df = generate_report(conn, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))    
        filtered_df = report_df[report_df['Component Name'] == selected_component_name] 
        if not filtered_df.empty:
            grouped_df = filtered_df.groupby(['Worker Name'])['Time Spent'].sum().reset_index()
            fig = px.bar(grouped_df, x='Worker Name', y='Time Spent',
                         title=f'Tiempo Total Gastado por Trabajador en {selected_component_name}',
                         labels={'Time Spent': 'Tiempo Gastado (horas)', 'Worker Name': 'Trabajador'},
                         color='Time Spent', 
                         color_continuous_scale=px.colors.sequential.Viridis)  
            fig.update_layout(
                xaxis_title="Trabajador",
                yaxis_title="Tiempo Gastado (horas)",
                plot_bgcolor='rgba(0,0,0,0)', 
                xaxis_tickangle=-45, 
                template='plotly_white', 
            )
            st.plotly_chart(fig)
        else:
            st.write("No hay datos disponibles para el componente seleccionado en el rango de fechas dado.")