import math

radio= float(input("Introduzca el radio de la circunferencia:"))

longitud = 2* math.pi * radio
area = math.pi * radio**2

print("Longitud: ", longitud, ", Área: ", area, sep="")

