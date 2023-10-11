"""
Escribe una función num_vocales(palabra) que devuelva el número de vocales que aparece en la palabra.
"""

def num_vocales_primera_v(palabra):
    contador = 0
    for i in palabra:
        if i in "aeiouAEIOU":
            contador += 1
    return contador

def num_vocales_segunda_v(palabra):
    contador = 0
    for i in palabra:
        if i.lower() in "aeiou":
            contador += 1
    return contador


palabra = input("Introduce una palabra: ")

print("Primera version")
print("La palabra", palabra, "tiene", num_vocales_primera_v(palabra), "vocales")

print("Segunda version")
print("La palabra", palabra, "tiene", num_vocales_segunda_v(palabra), "vocales")
