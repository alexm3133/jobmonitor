from database.repository import get_entries, delete_entry
import streamlit as st
import pandas as pd
 
def gestionar_entradas_tiempos(conn): 
    """
    Function to manage entries and times.

    Parameters:
    - conn: The database connection object.

    Returns:
    None
    """
    st.header("Gestionar entradas")
    entries = get_entries(conn)
    entries_df = pd.DataFrame(entries, columns=['Componente', 'Codification', 'Empleado', 'Fecha inicio', 'Fecha fin', 'Qt', 'Tiempo Total', 'Tiempo medio'])
    st.dataframe(entries_df)
    
    """ PENDIENTE IMPLEMENTAR
    entry_id_to_edit_or_delete = st.number_input("Enter ID of entry to edit or delete", min_value=0, format="%d", key="edit_delete")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete", key="delete"):
            delete_entry(conn, entry_id_to_edit_or_delete)
            st.success(f"Entry {entry_id_to_edit_or_delete} deleted successfully!")
    with col2:
        if st.button("Edit", key="edit"):
            pass
"""