"""
9. Escribe una función elimina_vocales(palabra) que elimine todas las vocales que aparecen en la palabra.
"""

def elimina_vocales_primera_v(palabra):
    nueva_palabra = ""
    for i in palabra:
        if i not in "aeiouAEIOU":
            nueva_palabra += i
    return nueva_palabra

def elimina_vocales_segunda_v(palabra):
    nueva_palabra = ""
    for i in palabra:
        if i.lower() not in "aeiou":
            nueva_palabra += i
    return nueva_palabra


palabra = input("Introduce una palabra: ")

print("Primera version")
print("La palabra", palabra, "sin vocales es", elimina_vocales_primera_v(palabra))

print("Segunda version")
print("La palabra", palabra, "sin vocales es", elimina_vocales_segunda_v(palabra))

