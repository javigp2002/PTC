# SAlidas de datos por pantalla de 4 maneras distintas

import math

radio = float(input("Introduzca el radio de la circunferencia:"))

area = math.pi * radio ** 2
print("El área del circulo con radio:", radio, " es: ", area)

print("El área del circulo con radio: %.2f es: %.2f" % (radio, area))

print("El área del circulo con radio:", round(radio, 2), " es: ", round(area, 2))

print(f"El área del circulo con radio: {radio:.2f} es: {area:.2f}")
