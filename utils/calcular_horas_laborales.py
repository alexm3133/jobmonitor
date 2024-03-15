from datetime import datetime, time, timedelta

def calcular_horas_laborales(start, end):
    # Define el horario laboral
    hora_inicio_laboral = time(6, 30)
    hora_fin_laboral = time(14, 30)
    
    # Inicializa el total de segundos trabajados
    total_segundos = 0
    
    # Procesa cada día
    current = start
    while current < end:
        # Si es día laboral
        if current.weekday() < 5: # Lunes a Viernes
            inicio_del_dia = datetime.combine(current.date(), hora_inicio_laboral)
            fin_del_dia = datetime.combine(current.date(), hora_fin_laboral)
            # Calcula inicio y fin efectivos dentro del horario laboral
            inicio_efectivo = max(current, inicio_del_dia)
            fin_efectivo = min(end, fin_del_dia)
            # Suma los segundos trabajados en el día
            if inicio_efectivo < fin_efectivo:
                total_segundos += (fin_efectivo - inicio_efectivo).total_seconds()
        
        # Avanza al siguiente día
        current += timedelta(days=1, seconds=-current.second, minutes=-current.minute, hours=-current.hour)
    
    horas_trabajadas = total_segundos / 3600
    return horas_trabajadas

def segundos_a_horas_minutos(total_segundos):
    horas = total_segundos // 3600
    minutos = (total_segundos % 3600) // 60
    return horas, minutos

