"""
2. Crea una lista con los valores enteros de 1 a N e implementa una función que reciba dicha lista y
nos devuelva una lista con los valores impares y el número de dichos valores. Solicitar N por
teclado y mostrar el resultado por pantalla

"""


def impares_lista(lista):
    impares = []
    num_impares = 0
    for i in lista:
        if i % 2 != 0:
            impares.append(i)
            num_impares += 1

    return impares, num_impares


def impares_lista_segundo(lista):
    var = [i for i in lista if i % 2 != 0]
    return var, len(var)


# main
lista = []
N = int(input("Introduce un número: "))
for i in range(1, N + 1):
    lista.append(i)

print("Los valores impares de la lista son:")
print("1º -> ", impares_lista(lista))
print("2º -> ", impares_lista_segundo(lista))

