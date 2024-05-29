import streamlit as st
from auth.auth import authenticate_user, register_user

def login_page():
    st.title("Iniciar Sesión / Registrarse")
    
    choice = st.radio("Elige una opción:", ("Iniciar Sesión", "Registrarse"))

    if choice == "Iniciar Sesión":
        with st.form("login_form"):
            worker_code = st.text_input("Código de Trabajador", max_chars=10, help="Introduce tu código de trabajador")
            password = st.text_input("Contraseña", type="password", help="Introduce tu contraseña")
            login_button = st.form_submit_button("Iniciar Sesión")
            if login_button:
                if authenticate_user(worker_code, password):
                    st.session_state['authenticated'] = True
                    st.success("Inicio de sesión exitoso")
                else:
                    st.error("Código de trabajador o contraseña incorrectos")

    elif choice == "Registrarse":
        with st.form("register_form"):
            new_worker_code = st.text_input("Nuevo Código de Trabajador", max_chars=10, help="Crea tu código de trabajador")
            new_worker_name = st.text_input("Nombre del Trabajador", help="Introduce tu nombre completo")
            new_password = st.text_input("Nueva Contraseña", type="password", help="Crea tu contraseña")
            register_button = st.form_submit_button("Registrarse")
            if register_button:
                if register_user(new_worker_code, new_worker_name, new_password):
                    st.success("Usuario registrado exitosamente")
                else:
                    st.error("Error al registrar el usuario")