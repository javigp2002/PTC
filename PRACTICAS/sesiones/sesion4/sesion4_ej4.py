"""
4. Usando el módulo “random” genera dos listas de N y M números enteros aleatorios entre 1 y 10 e
implementa una función que devuelva una tercera lista que contenga los números de las dos
primeras listas en orden ascendente sin contener valores repetidos. Solicitar N y M por teclado y
mostrar el resultado por pantalla.
"""

import random

def lista_aleatoria(N):
    return [random.randint(1, 10) for i in range(N)]

def ordenar_lista(lista):
    for i in range(0, len(lista)):
        min = lista[i]
        pos_min = i
        for j in range(i, len(lista)):
            if min > lista[j]:
                min = lista[j]
                pos_min = j

        if min != lista[i]:
            lista[pos_min], lista[i] = lista[i], lista[pos_min]

    return lista

def eliminar_duplicados(lista):
    lista_sin_duplicados = []
    for i in lista:
        if i not in lista_sin_duplicados:
            lista_sin_duplicados.append(i)

    return lista_sin_duplicados

def lista_concatenada(lista1, lista2):
    lista = lista1 + lista2
    lista = ordenar_lista(lista)
    lista = eliminar_duplicados(lista)

    return lista

def lista_concatenada_segunda(lista1, lista2):
    lista = lista1 + lista2
    lista.sort()
    #elimina los duplicados
    lista = list(dict.fromkeys(lista))

    return lista


# main
N = int(input("Introduce un número: "))
M = int(input("Introduce otro número: "))
lista1 = lista_aleatoria(N)
lista2 = lista_aleatoria(M)

print("La lista 1 es: ", lista1)
print("La lista 2 es: ", lista2)

print("La lista concatenada y ordenada es: ")
print("1º -> ",lista_concatenada(lista1, lista2))
print("2º -> ", lista_concatenada_segunda(lista1, lista2))

