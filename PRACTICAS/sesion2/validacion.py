"""
Ejercicio 1. Validar entradas de euros
"""

import math

def leer_euros():
    valido = False
    while not valido:
        euros = input("Introduzca la cantidad de euros: ")
        if euros:
            i=0
            punto = False
            valido = True
            while i < len(euros) and valido:
                if euros[i].isdigit():
                    valido= True
                else:
                    if euros[i] == "." and not punto:
                        punto = True
                        valido = True
                    else:
                        valido = False
                i+=1

            if valido and punto:
                lista = euros.split(".")
                if len(lista[1]) <= 0  or len(lista[1])>= 3:
                    valido = False

    return float(euros)

euros = leer_euros()
print("Validado:", euros)





