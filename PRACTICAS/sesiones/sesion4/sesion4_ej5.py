"""
Partiendo de una lista que contiene a su vez N listas de M enteros, si la consideramos como una
matriz de dimensión NxM, implementar una función que nos devuelva la matriz traspuesta MxN
(intercambiando filas y columnas) que contedrá M listas de N enteros. Solicitar N y M por teclado y
mostrar el resultado por pantalla.
"""

import random
def lista_aleatoria(N):
    return [random.randint(1, 10) for i in range(N)]

def matriz_traspuesta(matriz):
    matriz_traspuesta = []
    for i in range(len(matriz[0])):
        matriz_traspuesta.append([])
        for j in range(len(matriz)):
            matriz_traspuesta[i].append(matriz[j][i])

    return matriz_traspuesta

def matriz_traspuesta_segunda(matriz):
        return [[fila[i] for fila in matriz] for i in range(len(matriz[0]))]

# main
N = int(input("Introduce un número: "))
M = int(input("Introduce otro número: "))
matriz = []
for i in range(M):
    matriz.append(lista_aleatoria(N))

print("La matriz es: ", matriz)
print("La matriz traspuesta es: ")
print("1º -> ", matriz_traspuesta(matriz))
print("2º -> ", matriz_traspuesta_segunda(matriz))