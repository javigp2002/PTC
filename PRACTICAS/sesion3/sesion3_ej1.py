"""
1. Escribe una función contar_letras(palabra, letra)
que devuelva el número de veces que aparece una letra en una palabra
"""

def contar_letras_primera_v(palabra, letra):
    contador = 0
    for i in palabra:
        if i == letra:
            contador += 1
    return contador

def contar_letras_segunda_v(palabra,letra):
    return palabra.count(letra)


palabra = input("Introduce una palabra: ")
letra = input("Introduce una letra: ")

print("Primera version")
print("La letra", letra, "aparece", contar_letras_primera_v(palabra, letra), "veces en la palabra", palabra)

print("Segunda version")
print("La letra", letra, "aparece", contar_letras_segunda_v(palabra, letra), "veces en la palabra", palabra)