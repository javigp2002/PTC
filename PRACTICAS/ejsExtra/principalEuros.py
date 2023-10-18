"""
Debe pedir por teclado una cantidad de dinero en euros, un interes anual en tanto por ciento y un
número de años. Todos los valores deben pasar por un mecanismo de validación de modo que solo
admita valores válidos como por ejemplo, capital: 5689.34 interés en %: 10.05 años: 12.
El programa debe darnos como respuesta el capital acumulado, aplicando el interés anual durante el
número de años indicado, usando las funciones del módulo financiacion.py
"""

from financiacion import calcularCapitalAnual, leerInt, leerFloat2decimales


capitalInicial = leerFloat2decimales()
interes = leerFloat2decimales()
anios = leerInt()

capitalAcumulado = capitalInicial
for i in range(anios):
    capitalAcumulado = calcularCapitalAnual(capitalAcumulado, interes)

print("Capital acumulado: ", capitalAcumulado)

