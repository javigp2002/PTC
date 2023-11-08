"""
1. Crea una lista con los valores enteros de 1 a N e implementa una función que reciba dicha lista y
nos devuelva la suma de dichos valores. Solicitar N por teclado y mostrar el resultado por pantalla.
"""


def suma_lista(lista):
    suma = 0
    for i in lista:
        suma += i
    return suma


def suma_lista_segundo(lista):
    return sum(lista)

# main
lista = []
N = int(input("Introduce un número: "))
for i in range(1, N + 1):
    lista.append(i)

print("La suma de los valores de la lista es:")
print("1º -> ", suma_lista(lista))
print("2º -> ", suma_lista_segundo(lista))
