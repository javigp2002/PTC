"""
10. Escribe una función es_inversa(palabra1, palabra2) que determine si una palabra es la misma que la otra pero con los
 caracteres en orden inverso. Por ejemplo 'absd' y 'dsba'.
"""

def es_inversa(palabra1, palabra2):
    return palabra1 == palabra2[::-1]

def es_inversa_v2(palabra1, palabra2):
    if (len(palabra1) != len(palabra2)):
        return False
    else:
        longPalabra=len(palabra1)
        i=0
        while i < longPalabra:
            if palabra1[i] == palabra2[longPalabra-i-1]:
                i += 1
            else:
                return False
        return True


palabra1 = input("Introduce una palabra: ")
palabra2 = input("Introduce otra palabra: ")

print("Primera version")
if es_inversa(palabra1, palabra2):
    print("La palabra", palabra1, "es inversa de", palabra2)
else:
    print("La palabra", palabra1, "no es inversa de", palabra2)

print("Segunda version")
if es_inversa_v2(palabra1, palabra2):
    print("La palabra", palabra1, "es inversa de", palabra2)
else:
    print("La palabra", palabra1, "no es inversa de", palabra2)