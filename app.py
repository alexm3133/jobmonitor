import streamlit as st
from streamlit_option_menu import option_menu
from database.database_connection import create_connection, setup_database
from components.gestion_tiempos_soldadura import gestion_tiempos_soldadura
from components.administrar_componentes import administrar_componentes
from components.administrar_trabajadores import administrar_trabajadores
from components.gestionar_entradas import gestionar_entradas
from auth.auth import logout
from components.login import login_page

# Initialize the database
database = "soldering_db.sqlite"
conn = create_connection(database)
setup_database(conn)

# Main application function
def app():
    # Check user priority and display options based on that
    user_priority = st.session_state.get('user_priority', 2)  # Default to priority 2 if not set
    if user_priority == 1:
        # Full menu options for priority 1 users
        menu_options = {
            "Gestion Tiempos Soldadura": gestion_tiempos_soldadura,
            "Historial": gestionar_entradas,
            "Administrar Componentes": administrar_componentes,
            "Administrar Trabajadores": administrar_trabajadores,
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
            "Hola": lambda: st.sidebar.write("¡Hola! No tienes acceso a las funciones administrativas.")
        }
        
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
