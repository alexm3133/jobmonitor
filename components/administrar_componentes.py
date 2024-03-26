from database.repository import (get_machines, add_machine, get_components, add_component, 
                                 add_codification, get_codifications_for_component, 
                                 add_machine_component, component_exists_in_machine)
import streamlit as st

def administrar_componentes(conn):
    st.header("Administrar Componentes y Máquinas")
    component_id = None  # Inicializar component_id con None

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

    # Si se ha seleccionado o añadido una máquina, gestionar componentes
    if selected_machine_id:
        component_name = st.text_input("Nombre del Nuevo Componente", "")
        if st.button("Añadir Nuevo Componente"):
            # Verificar si el componente ya existe en la máquina seleccionada
            if not component_exists_in_machine(conn, selected_machine_id, component_name):
                component_id = add_component(conn, component_name)
                if component_id:
                    add_machine_component(conn, selected_machine_id, component_id)
                    st.success(f"Componente '{component_name}' añadido correctamente.")
                else:
                    st.error("Error añadiendo componente.")
            else:
                st.error("El componente ya existe en esta máquina.")

        # Mostrar y añadir codificaciones para el componente seleccionado
        existing_components = get_components(conn, selected_machine_id)
        existing_component_names = [component[1] for component in existing_components]
        component_selection = st.selectbox("Seleccionar Componente Existente", ["Elija un componente"] + existing_component_names)
        
        if component_selection != "Elija un componente":
            component_id = next((comp[0] for comp in existing_components if comp[1] == component_selection), None)

        if component_id:
            codification_text = st.text_input("Añadir Nueva Codificación", "")
            if st.button("Añadir Codificación") and codification_text:
                success = add_codification(conn, selected_machine_id, component_id, codification_text)
                if success:
                    st.success("Codificación añadida correctamente al componente.")
                else:
                    st.error("Error añadiendo codificación al componente.")
            
            # Mostrar codificaciones existentes para el componente seleccionado
            existing_codifications = get_codifications_for_component(conn, selected_machine_id, component_id)
            st.write("Codificaciones existentes:")
            for codification in existing_codifications:
                st.write(f"- {codification}")
