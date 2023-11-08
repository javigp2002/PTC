"""
EJECICIO EXTRA SOBRE VALIDACIÓN
Hay que realizar un script llamado validarEurosExcepciones.py que realice la validación con la sentencia de gestión de excepciones


Vemos si es un digito numérico y formato 99.99. Sirve para euros e interés.
Se queda pidiendo el dato hasta que esté correcto y devuelve el float positivo con dos decimales.
    o Entrada: mensaje para pedir el dato concreto.
    o Salida: valorValidado, numeroIntentosIncorrectos.
"""


def leerFloatMax2Decimales(mensaje):
    correcto = False
    nIncorrectas = 0
    valor = 0
    while not correcto:
        try:
            entrada = (input(mensaje))
            valor = float(entrada)
            assert valor > 0, f"\tLa entrada debe ser mayor a cero y ha indicado {valor}"

            longitudDecimales = len(entrada.split(".")[1])
            assert longitudDecimales <= 2, (f"\tLa entrada debe tener MÁXIMO dos decimales y ha indicado {longitudDecimales} decimales"
                                            f" en {entrada}")

            print(f"\tLa entrada es {valor} y es correcta")
            correcto = True
        except ValueError:
            print(f"\tDebe introducir un número decimal y su entrada fue: '{entrada}'")
            nIncorrectas += 1
        except AssertionError as error:
            print(error)
            nIncorrectas += 1

    return valor, nIncorrectas


"""
Vemos si es un digito numérico entero (sin decimales) y positivo. Se queda pidiendo el dato hasta que esté correcto y 
devuelve el entero positivo.
    o Entrada: mensaje para pedir el dato concreto.
    o Salida: valorValidado, numeroIntentosIncorrectos.
"""


def leerEnteroPositivo(mensaje):
    correcto = False
    nIncorrectas = 0
    while not correcto:
        try:
            entrada = (input(mensaje))
            valor = int(entrada)

            assert valor > 0, f"\tLa entrada debe ser mayor a cero y ha indicado {valor}"

            print(f"\tLa entrada es {valor} y es correcta")
            correcto = True
        except ValueError:
            print(f"\tDebe introducir un número entero y su entrada fue: '{entrada}'")
            nIncorrectas += 1
        except AssertionError as error:
            print(error)
            nIncorrectas += 1

    return valor, nIncorrectas


if __name__ == "__main__":
    nombreEstudiante = "Javier González Peregrín"
    nCorrectas = 0
    nIncorrectas = 0

    capital, nInc = leerFloatMax2Decimales("Dime capital inicial con 2 decimales máximo: ")
    nCorrectas += 1
    nIncorrectas = nIncorrectas + nInc

    interés, nInc = leerFloatMax2Decimales("Dime interés anual con 2 decimales máximo: ")
    nCorrectas += 1
    nIncorrectas = nIncorrectas + nInc

    anios, nInc = leerEnteroPositivo("Dime el número de años: ")
    nCorrectas += 1

    nIncorrectas = nIncorrectas + nInc

    print("Fin del programa de validación de euros")
    print("Nombre estudiante: ", nombreEstudiante)
    print("Entradas correctas: ", nCorrectas, " incorrectas: ", nIncorrectas)
