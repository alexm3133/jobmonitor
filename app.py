import streamlit as st
from streamlit_option_menu import option_menu
from database.database_connection import create_connection, setup_database
from components.gestion_tiempos_soldadura import gestion_tiempos_soldadura
from components.gestionar_entradas_tiempos import gestionar_entradas_tiempos
from components.generar_graficos import generar_graficos
from components.administrar_componentes import administrar_componentes
from components.administrar_trabajadores import administrar_trabajadores

# Initialize the database
database = "soldering_db.sqlite"
conn = create_connection(database)
setup_database(conn)

def authenticate_user(user_code, password):
    """Authenticate a user based on their worker code and password."""
    sql = ''' SELECT * FROM users WHERE trabajador_code=? AND trabajador_password=? '''
    cur = conn.cursor()
    cur.execute(sql, (user_code, password))
    account = cur.fetchone()
    return account is not None

def logout():
    st.session_state['authenticated'] = False
    st.experimental_rerun()

# Main application function
def app():
    menu_options = {
        "Gestion Tiempos Soldadura": gestion_tiempos_soldadura,
        "Gestionar Entradas": gestionar_entradas_tiempos,
        "Generar Reporte": generar_graficos,
        "Administrar Componentes": administrar_componentes,
        "Administrar Trabajadores": administrar_trabajadores,
    }

    menu_icons = ["tools", "clipboard-data", "graph-up", "puzzle", "person"]

    with st.sidebar:
        selected_option = option_menu("Menú Principal", list(menu_options.keys()), 
                                      icons=menu_icons, menu_icon="cast", default_index=0)

    if selected_option:
        menu_options[selected_option](conn)
    if st.sidebar.button("Logout"):
        logout()

# Login page
def login_page():
    st.title("Login Page")
    with st.form("login_form"):
        trabajador_code = st.text_input("Worker Code")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")
        if login_button:
            if authenticate_user(trabajador_code, password):
                st.session_state['authenticated'] = True
            else:
                st.error("Invalid credentials")

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Check if user is authenticated before showing the app
if st.session_state['authenticated']:
    app()
else:
    login_page()
