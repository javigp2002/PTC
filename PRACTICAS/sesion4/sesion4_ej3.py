"""
3. Crea una lista con los valores enteros de 1 a N e implementa una función que reciba dicha lista y
nos devuelva el máximo y el mínimo de dichos valores, así como sus respectivas posiciones.
Solicitar N por teclado y mostrar el resultado por pantalla.
"""

def max_min_lista(lista):
    maximo = lista[0]
    minimo = lista[0]
    pos_max = 0
    pos_min = 0

    index = 0
    for i in lista:
        if i > maximo:
            maximo = i
            pos_max = lista.index(i)
        if i < minimo:
            minimo = i
            pos_min = lista.index(i)
        index += 1

    return maximo, pos_max, minimo, pos_min

def max_min_lista_segundo(lista):
    return max(lista), lista.index(max(lista)), min(lista), lista.index(min(lista))


# main
lista = []
N = int(input("Introduce un número: "))
for i in range(1, N + 1):
    lista.append(i)

print("El (máximo, posicion) y el (mínimo, posicion) de los valores de la lista son:")
print("1º -> ", max_min_lista(lista))
print("2º -> ", max_min_lista_segundo(lista))
