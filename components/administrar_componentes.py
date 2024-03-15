from database.repository import get_components, add_component, add_codification
import streamlit as st

def administrar_componentes(conn):
    st.header("Administrar Componentes")
    # Inicializar component_id como None
    component_id = None
    # Paso 1: Seleccionar o Añadir un nuevo Componente
    existing_components = get_components(conn)  # Asume que esta función devuelve una lista de tuplas (id, name)
    existing_component_names = [component[1] for component in existing_components]
    component_selection = st.selectbox("Seleccionar Componente Existente", ["Nuevo Componente"] + existing_component_names)
    if component_selection == "Nuevo Componente":
        component_name = st.text_input("Nombre del Nuevo Componente", "")
        if st.button("Añadir Nuevo Componente"):
            component_id = add_component(conn, component_name)
            if component_id:
                st.success(f"Componente '{component_name}' añadido correctamente.")
            else:
                st.error("Error añadiendo componente.")
    else:
        component_id = next((comp[0] for comp in existing_components if comp[1] == component_selection), None)
    
    # Paso 2: Añadir Codificación al Componente Seleccionado
    if component_id:
        st.write(f"Componente Seleccionado: {component_selection if component_selection != 'Nuevo Componente' else component_name}")
        codification_text = st.text_input("Añadir Nueva Codificación", "")
        if st.button("Añadir Codificación"):
            if add_codification(conn, component_id, codification_text):
                st.success("Codificación añadida correctamente al componente.")
            else:
                st.error("Error añadiendo codificación al componente.")

