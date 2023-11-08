"""
Realizar un programa que pida el nombre de una persona, primer apellido, segundo apellido y
que muestre por pantalla como sería el nombre completo en una sola línea. También mostrar el
nombre completo pero al revés. Finalmente volver a descomponer el nombre completo en sus tres
componentes y mostrarlos por pantalla.
"""

nombre = str(input("Introduzca el nombre:"))
apellido1 = str(input("Introduzca el primer apellido:"))
apellido2 = str(input("Introduzca el segundo apellido:"))

nombre_completo = nombre + " " + apellido1 + " " + apellido2
#print(nombre, apellido1, apellido2, sep=" ")
print(nombre_completo)

print(nombre_completo[::-1])

nombre_completo = nombre_completo.split(" ")
print(nombre_completo[0], nombre_completo[1], nombre_completo[2], sep=" ")