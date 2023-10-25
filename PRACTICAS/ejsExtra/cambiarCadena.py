# quitar la letra A mayuscula

cadena = "HoAla muAndoAA a todos"
i=0
while (i < len(cadena)):
    if cadena[i] == "A":
        cadena = cadena[:i] + cadena[i+1:]
    else:
        i += 1

print(cadena)