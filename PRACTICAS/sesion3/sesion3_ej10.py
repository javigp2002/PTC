"""
10. Escribe una función es_inversa(palabra1, palabra2) que determine si una palabra es la misma que la otra pero con los
 caracteres en orden inverso. Por ejemplo 'absd' y 'dsba'.
"""

def es_inversa_primera_v(palabra1, palabra2):
    if palabra1 == palabra2[::-1]:
        return True
    else:
        return False

