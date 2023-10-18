"""
Debe contener, al menos, las siguiente funciones en python
leerFloat2decimales() #Vemos si es un digito numérico y formato 99.99. Sirve para euros e interés
Se queda pidiendo el dato hasta que esté correcto y devuelve el float con dos decimales

leerInt() #Vemos si es un digito numérico entero (sin decimales) y positivo
Se queda pidiendo el dato hasta que esté correcto y devuelve el entero

redondear(numero, decimales)
entrada: un float y la cantidad de decimales a redondear (usaremos 2)
salida: un float redondeado hacia arriba a partir de 0.5 (como en el caso de los euros)

calcularCapitalAnual(capitalInicial, interes)
entrada: un float en euros, con dos decimales, y un interés en tanto por cien con dos decimales
salida: suma de capital inicial + interes obtenido
es decir capitalAnual=capitalInicial+capitalInicial*interes/100.
la salida tiene que estar redondeada a 2 decimales pues estamos trabajando en euros
"""

# Vemos si es un digito numérico y formato 99.99. Sirve para euros e interés
def leerFloat2decimales():
    valido = False
    while not valido:
        euros = input("Introduzca la un float con 2 decimales: ")
        if euros:
            i = 0
            punto = False
            valido = True
            while i < len(euros) and valido:
                if euros[i].isdigit():
                    valido = True
                else:
                    if euros[i] == "." and not punto:
                        punto = True
                        valido = True
                    else:
                        valido = False
                i += 1

            if valido and punto:
                lista = euros.split(".")
                if len(lista[1]) <= 0 or len(lista[1]) >= 3:
                    valido = False

    return float(euros)

def leerInt():
    valido = False
    while not valido:
        euros = input("Introduzca un dígicto numérico entero: ")
        if euros:
            i = 0
            valido = True
            while i < len(euros) and valido:
                if euros[i].isdigit():
                    valido = True
                else:
                    valido = False
                i += 1

    return int(euros)


def redondear(numero, decimales=2):
    numero = numero * (10 ** decimales)
    numero = numero + 0.5
    numero = (int)(numero)
    numero = numero / (10 ** decimales)
    return numero


def calcularCapitalAnual(capitalInicial, interes):
    capitalAnual = capitalInicial + capitalInicial * interes / 100

    return redondear(capitalAnual, 2)