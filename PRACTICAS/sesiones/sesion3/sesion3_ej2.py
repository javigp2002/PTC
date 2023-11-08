"""
2. Escribe una función eliminar_letras(palabra, letra) que devuelva una
versión de palabra que no contiene el carácter letra ninguna vez.
"""

def eliminar_letras_primera_version(palabra, letra):
    nueva_palabra = ""
    for i in palabra:
        if i != letra:
            nueva_palabra += i
    return nueva_palabra

def eliminar_letras_segunda_version(palabra, letra):
    return palabra.replace(letra, "")

palabra = input("Introduce una palabra: ")
letra = input("Introduce una letra: ")

print("Primera version")
print("La palabra", palabra, "sin la letra", letra, "es", eliminar_letras_primera_version(palabra, letra))

print("Segunda version")
print("La palabra", palabra, "sin la letra", letra, "es", eliminar_letras_segunda_version(palabra, letra))
