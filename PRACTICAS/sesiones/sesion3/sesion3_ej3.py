"""
3. Escribe una función mayusculas_minusculas(palabra) que devuelva una cadena en la
 que las mayúsculas y las minúsculas estén al contrario.
"""

#version sin usar supper o lower
def mayus_minus_primera_version(palabra):
    nueva_palabra = ""
    for i in palabra:
        if i >= "A" and i <= "Z":
            nueva_palabra += chr(ord(i) + 32)
        else:
            nueva_palabra += chr(ord(i) - 32)
    return nueva_palabra

def mayus_minus_segunda_version(palabra):
    return palabra.swapcase()


palabra = input("Introduce una palabra: ")

print("Primera version")
print("La palabra", palabra, "con las mayusculas y minusculas cambiadas es", mayus_minus_primera_version(palabra))

print("Segunda version")
print("La palabra", palabra, "con las mayusculas y minusculas cambiadas es", mayus_minus_segunda_version(palabra))