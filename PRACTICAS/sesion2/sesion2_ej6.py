"""
 Pedir tres valores reales x1,x2,x3, obtener su máximo y su mínimo y mostrarlos por pantalla. (No
usar la funcion max y min de python).
"""

x1 = int(input("Introduzca el primer número:"))
x2 = int(input("Introduzca el segundo número:"))
x3 = int(input("Introduzca el tercer número:"))

if x1 > x2:
    maximo = x1
    minimo = x2
else:
    maximo = x2
    minimo = x1

if x3 > maximo:
    maximo = x3
elif x3 < minimo:
    minimo = x3

print("El máximo es", maximo, "y el mínimo es", minimo)
