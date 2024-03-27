import streamlit as st

def utilidades(conn=None):
    #como poner el titulo en bold
    st.title('Utilidades')
    st.title("Calcular precios con iva")
    # podremos anadir en una casilla precio sin iva, y devolvera el precio con iva que 21% primero crear una casilla para coger el precio sin iva
    precio_sin_iva = st.number_input("Precio sin IVA", min_value=0.0, value=0.0, step=1.0)
    precio_con_iva = precio_sin_iva * 1.21
    st.write(f"Precio con IVA: {precio_con_iva}")

    st.title("Convertir a horas y minutos")
    # Convertir el valor total en horas a minutos primero
    total_minutos = st.number_input("Total en minutos", min_value=0, value=0, step=1)
    horas = int(total_minutos // 60)
    minutos = int(total_minutos % 60)
    st.write(f"{horas}h {minutos}min")
