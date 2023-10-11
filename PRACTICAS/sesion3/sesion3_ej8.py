"""
8. Escribe una función inicio_fin_vocal(palabra) que determine si una palabra empieza y acaba con una vocal.
"""

def inicio_fin_vocal_primera_v(palabra):
    if palabra[0] in "aeiouAEIOU" and palabra[-1] in "aeiouAEIOU":
        return True
    else:
        return False


def inicio_fin_vocal_segunda_v(palabra):
    if palabra[0].lower() in "aeiou" and palabra[-1].lower() in "aeiou":
        return True
    else:
        return False


palabra = input("Introduce una palabra: ")

print("Primera version")
if inicio_fin_vocal_primera_v(palabra):
    print("La palabra", palabra, "empieza y acaba por vocal")
else:
    print("La palabra", palabra, "no empieza y acaba por vocal")

print("Segunda version")
if inicio_fin_vocal_segunda_v(palabra):
    print("La palabra", palabra, "empieza y acaba por vocal")
else:
    print("La palabra", palabra, "no empieza y acaba por vocal")

