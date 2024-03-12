import streamlit as st
from database.database import create_connection, add_component, get_components, add_entry, get_entries, delete_entry, generate_report
import pandas as pd

from datetime import datetime, timedelta


database = "soldering_db.sqlite"
conn = create_connection(database)

menu_options = ["Soldering Time Tracker", "Manage Entries", "Generate Report", "Administrar Componentes"]
selected_option = st.sidebar.selectbox("Menu", menu_options)

if selected_option == "Soldering Time Tracker":
    st.title('Soldering Time Tracker')
    worker_name = st.text_input("Worker Name", "")
    components = get_components(conn)
    component_options = {comp[1]: comp[0] for comp in components}  # component_name: component_id
    selected_component = st.selectbox("Component", list(component_options.keys()))
    selected_component_id = component_options[selected_component]
    time_spent = st.number_input("Time Spent (Hours)", min_value=0.0, format="%.2f")
    date = st.date_input("Date", datetime.now())
    if st.button("Submit"):
        add_entry(conn, worker_name, selected_component_id, time_spent, date.strftime("%Y-%m-%d"))
        st.success("Entry added successfully!")

elif selected_option == "Manage Entries":
    st.header("Manage Entries")
    entries = get_entries(conn)
    entries_df = pd.DataFrame(entries, columns=['ID', 'Date', 'Time Spent', 'Component Name', 'Component Code', 'Worker Name'])
    st.dataframe(entries_df)
    entry_id_to_edit_or_delete = st.number_input("Enter ID of entry to edit or delete", min_value=0, format="%d", key="edit_delete")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete", key="delete"):
            delete_entry(conn, entry_id_to_edit_or_delete)
            st.success(f"Entry {entry_id_to_edit_or_delete} deleted successfully!")
    with col2:
        if st.button("Edit", key="edit"):
            pass
elif selected_option == "Generate Report":
    st.header("Generate Report")
    start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    end_date = st.date_input("End Date", datetime.now())
    if st.button("Generate"):
        report_df = generate_report(conn, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        st.dataframe(report_df)
        # Optional: Add visualization code here

elif selected_option == "Administrar Componentes":
    st.header("Administrar Componentes")
    component_name = st.text_input("Nombre del Componente", "")
    component_code = st.text_input("Código del Componente", "")
    if st.button("Añadir Componente"):
        add_component(conn, component_name, component_code)
        st.success("Componente añadido correctamente.")

