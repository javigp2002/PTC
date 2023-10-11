"""
Partiendo de una disolución de ácido sulfúrico en agua al 80 % de concentración, quiero obtener
una cantidad x de centímetros cúbicos a una concentración y% (y<80%). Siendo x, e y valores de
entrada al programa, calcular cuantos centímetros cúbicos de la disolución al 80% y de agua son
necesarios para obtener los x centímetros cúbicos deseados al y% de concentración.
"""


volumen_final = float(input("Introduzca los cc finales:"))

concentracion_inicial = 80
concentracion_final = float(input("Introduzca el % de la concentracion final deseada:"))

volumen_inicial = volumen_final * concentracion_final / concentracion_inicial

volumen_agua = volumen_final - volumen_inicial

print("Se necesitan", volumen_inicial, "cc de la disolucion al 80% y", volumen_agua, "cc de agua")