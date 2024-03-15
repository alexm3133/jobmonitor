import streamlit as st
from streamlit_option_menu import option_menu
from database.database_connection import create_connection, setup_database
from components.gestion_tiempos_soldadura import gestion_tiempos_soldadura
from components.gestionar_entradas_tiempos import gestionar_entradas_tiempos
from components.generar_graficos import generar_graficos
from components.administrar_componentes import administrar_componentes
from components.administrar_trabajadores import administrar_trabajadores

# Conexión y configuración de la base de datos
database = "soldering_db.sqlite"
conn = create_connection(database)
setup_database(conn)

# Definición de las opciones del menú y sus respectivas funciones
menu_options = {
    "Gestion Tiempos Soldadura": gestion_tiempos_soldadura,
    "Gestionar Entradas": gestionar_entradas_tiempos,
    "Generar Reporte": generar_graficos,
    "Administrar Componentes": administrar_componentes,
    "Administrar Trabajadores": administrar_trabajadores,
}

# Asignación de iconos a las opciones del menú (ajusta los iconos según corresponda)
menu_icons = ["tools", "clipboard-data", "graph-up", "puzzle", "person"]

# Creación del menú de opciones usando streamlit-option-menu
with st.sidebar:
    selected_option = option_menu("Menú Principal", list(menu_options.keys()), 
                                  icons=menu_icons, menu_icon="cast", default_index=0)

# Ejecución de la función asociada a la opción seleccionada
if selected_option:
    menu_options[selected_option](conn)
