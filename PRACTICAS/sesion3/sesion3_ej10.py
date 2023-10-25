"""
10. Escribe una función es_inversa(palabra1, palabra2) que determine si una palabra es la misma que la otra pero con los
 caracteres en orden inverso. Por ejemplo 'absd' y 'dsba'.
"""

def es_inversa(palabra1, palabra2):
    return palabra1 == palabra2[::-1]

palabra1 = input("Introduce una palabra: ")
palabra2 = input("Introduce otra palabra: ")

print("Primera version")
if es_inversa(palabra1, palabra2):
    print("La palabra", palabra1, "es inversa de", palabra2)
else:
    print("La palabra", palabra1, "no es inversa de", palabra2)
