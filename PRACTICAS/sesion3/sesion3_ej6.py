"""
6. Escribe una función vocales(palabra) que devuelva las vocales que aparecen en la palabra.
"""

def vocales_primera_v(palabra):
    vocales = ""
    for i in palabra:
        if i in "aeiouAEIOU":
            vocales += i
    return vocales

def vocales_segunda_v(palabra):
    vocales = ""
    for i in palabra:
        if i.lower() in "aeiou":
            vocales += i
    return vocales


palabra = input("Introduce una palabra: ")

print("Primera version")
print("La palabra", palabra, "tiene las vocales", vocales_primera_v(palabra))

print("Segunda version")
print("La palabra", palabra, "tiene las vocales", vocales_segunda_v(palabra))

