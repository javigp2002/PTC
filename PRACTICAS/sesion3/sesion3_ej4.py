"""
Escribe una función buscar(palabra, sub) que devuelva la posición en la que se
puede encontrar sub dentro de palabra o -1 en caso de que no esté.
"""

def buscar_primera_version(palabra, sub):
    posicion = -1
    for i in range(len(palabra)):
        if palabra[i:i+len(sub)] == sub:
            posicion = i
    return posicion

def buscar_segunda_version(palabra, sub):
    return palabra.find(sub)


palabra = input("Introduce una palabra: ")
sub = input("Introduce una subcadena: ")

print("Primera version")
print("La subcadena", sub, "se encuentra en la posicion", buscar_primera_version(palabra, sub), "de la palabra", palabra)

print("Segunda version")
print("La subcadena", sub, "se encuentra en la posicion", buscar_segunda_version(palabra, sub), "de la palabra", palabra)
