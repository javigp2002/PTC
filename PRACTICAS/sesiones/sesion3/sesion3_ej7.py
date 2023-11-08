"""
7. Escribe una función mayusculas(palabra) que devuelva la palabra pasada a mayúsculas.
"""

def mayusculas_primera_v(palabra):
    nueva_palabra = ""
    for i in palabra:
        if i >= "a" and i <= "z":
            nueva_palabra += chr(ord(i) - 32)
        else:
            nueva_palabra += i
    return nueva_palabra

def mayusculas_segunda_v(palabra):
    return palabra.upper()


palabra = input("Introduce una palabra: ")

print("Primera version")
print("La palabra", palabra, "en mayusculas es", mayusculas_primera_v(palabra))

print("Segunda version")
print("La palabra", palabra, "en mayusculas es", mayusculas_segunda_v(palabra))


