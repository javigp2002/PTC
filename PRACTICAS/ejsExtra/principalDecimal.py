"""
En el tercer fichero llamado “principalDecimal.py” implementamos el mismo programa usando
las funciones de lectura de “financiacion.py” pero usando el modulo “decimal” y el tipo de dato
decimal.Decimal para calcular el capital cada año y tratar los valores en euros y comprobamos si
obtenemos las mismas salidas que con el fichero del punto 2 para las mismas entradas en varios
casos
"""
import decimal
from decimal import Decimal, getcontext
from financiacion import leerInt, leerFloat2decimales

def redondearCentesimas(numero):
    getcontext().rounding = decimal.ROUND_HALF_UP
    x = Decimal(numero)
    return x.quantize(Decimal("1.00"))


def calcularCapitalAnual(capitalInicial, interes):
    capitalAnual = capitalInicial + capitalInicial * interes / 100

    return float(redondearCentesimas(capitalAnual))


## MAIN ##
capitalInicial = leerFloat2decimales()
interes = leerFloat2decimales()
anios = leerInt()

capitalAcumulado = capitalInicial
for i in range(anios):
    capitalAcumulado = calcularCapitalAnual(capitalAcumulado, interes)

print("Capital acumulado: ", capitalAcumulado)

