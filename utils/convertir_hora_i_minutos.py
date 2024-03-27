def convertir_a_horas_minutos(valor_en_horas):

    # Convertir el valor total en horas a minutos primero

    total_minutos = valor_en_horas * 60

    # Dividir los minutos totales para obtener horas y minutos

    horas = int(total_minutos // 60)

    minutos = int(total_minutos % 60)

    return f"{horas}h {minutos}min"