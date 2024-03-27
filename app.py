import streamlit as st
from streamlit_option_menu import option_menu
from database.database_connection import setup_database, create_connection
from components.gestion_tiempos_soldadura import gestion_tiempos_soldadura
from components.administrar_componentes import administrar_componentes
from components.administrar_trabajadores import administrar_workers
from components.historial import gestionar_entradas
from components.empleado import empleado
from components.utilidades import utilidades
from auth.auth import logout
from components.login import login_page


# Initialize the database
database = "soldering_db.sqlite"
conn = create_connection(database)
setup_database(conn)
st. set_page_config(layout="wide")
# Main application function
def app():
    # Check user priority and display options based on that
    user_priority = st.session_state.get('user_priority', 2)  # Default to priority 2 if not set
    if user_priority == 1:
        # Full menu options for priority 1 users
        menu_options = {
            "Historial": gestionar_entradas,
            "Gestion Tiempos Soldadura": gestion_tiempos_soldadura,
            "Administrar Componentes": administrar_componentes,
            "Administrar Trabajadores": administrar_workers,
            "Utilidades": utilidades
        }
        menu_icons = ["tools", "clipboard-data", "graph-up", "puzzle", "person"]
        with st.sidebar:
            selected_option = option_menu("Menú Principal", list(menu_options.keys()), 
                                        icons=menu_icons, menu_icon="cast", default_index=0)
        if selected_option:
            menu_options[selected_option](conn)
    else:
        # Only show a greeting for non-priority 1 users
        menu_options = {
            "Tu espacio": lambda: st.sidebar.write("¡Hola! No tienes acceso a las funciones administrativas.")
        }
        empleado(conn)
        
        menu_icons = ["emoji-smile"]
        with st.sidebar:
            selected_option = option_menu("Menú Principal", list(menu_options.keys()), 
                                        icons=menu_icons, menu_icon="cast", default_index=0)
      
    # Logout button
    if st.sidebar.button("Cerrar session"):
        logout()
    

# Authentication check before showing the app
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if st.session_state['authenticated']:
    app()
else:
    login_page()
