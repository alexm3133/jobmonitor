from database.repository import get_machines, add_machine, get_components, add_component, add_codification
import streamlit as st

def administrar_componentes(conn):
    st.header("Administrar Componentes y Máquinas")
    component_id = None
    # Añadir o seleccionar máquinas
    existing_machines = get_machines(conn)
    machine_options = {"Elija una máquina": None}
    machine_options.update({machine[1]: machine[0] for machine in existing_machines})
    selected_machine = st.selectbox("Seleccionar Máquina Existente", list(machine_options.keys()))
    selected_machine_id = machine_options[selected_machine]
    
    if selected_machine == "Elija una máquina":
        new_machine_name = st.text_input("Nombre de la Nueva Máquina", "")
        if st.button("Añadir Nueva Máquina"):
            selected_machine_id = add_machine(conn, new_machine_name)
            if selected_machine_id:
                st.success(f"Máquina '{new_machine_name}' añadida correctamente.")
            else:
                st.error("Error añadiendo máquina.")
    
    if selected_machine_id:
        existing_components = get_components(conn)  # Asegúrate de que esta función filtre por selected_machine_id si es necesario
        existing_component_names = [component[1] for component in existing_components]
        component_selection = st.selectbox("Seleccionar Componente Existente", ["Nuevo Componente"] + existing_component_names)

        if component_selection == "Nuevo Componente":
            component_name = st.text_input("Nombre del Nuevo Componente", "")
            if st.button("Añadir Nuevo Componente"):
                component_id = add_component(conn, selected_machine_id, component_name)
                if component_id:
                    st.success(f"Componente '{component_name}' añadido correctamente.")
                else:
                    st.error("Error añadiendo componente.")
        else:
            component_id = next((comp[0] for comp in existing_components if comp[1] == component_selection), None)

        if component_id:
            codification_text = st.text_input("Añadir Nueva Codificación", "")
            if st.button("Añadir Codificación"):
                success = add_codification(conn, component_id, codification_text)
                if success:
                    st.success("Codificación añadida correctamente al componente.")
                else:
                    st.error("Error añadiendo codificación al componente.")
