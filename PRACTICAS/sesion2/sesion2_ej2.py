"""
2. Dados tres números x1, x2, x3, calcular la desviación típica respecto a su media aritmética.


"""

import math

x1 = float(input("Introduzca el primer número:"))
x2 = float(input("Introduzca el segundo número:"))
x3 = float(input("Introduzca el tercer número:"))

n = 3
media_aritmetica = (x1 + x2 + x3) / n

desviacion_tipica = math.sqrt(((x1 - media_aritmetica)**2 + (x2 - media_aritmetica)**2 + (x3 - media_aritmetica)**2) / n)

print("La desviación típica es", round(desviacion_tipica,2), sep=" ")