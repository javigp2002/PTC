"""
Hacer un programa para calcular la diferencia en horas:minutos:segundos entre dos instantes de
tiempo dados en horas:minutos:segundos.
"""

horas_minutos_segundos_1 = str(input("Introduzca el primer tiempo en formato 'hh:mm:ss' "))
horas_minutos_segundos_2 = str(input("Introduzca el segundo tiempo en formato 'hh:mm:ss' "))

tiempo_1 = horas_minutos_segundos_1.split(":")
tiempo_2 = horas_minutos_segundos_2.split(":")

horas_1 = int(tiempo_1[0])
minutos_1 = int(tiempo_1[1])
segundos_1 = int(tiempo_1[2])

horas_2 = int(tiempo_2[0])
minutos_2 = int(tiempo_2[1])
segundos_2 = int(tiempo_2[2])

segundos_final_totales = segundos_2 - segundos_1 + (minutos_2 - minutos_1) * 60 + (horas_2 - horas_1) * 3600

minutos_final = segundos_final_totales // 60
segundos_final_totales = segundos_final_totales % 60

horas_final = minutos_final // 60
minutos_final = minutos_final % 60

print(horas_final, "horas,", minutos_final, "minutos y", segundos_final_totales, "segundos")