"""
4. Realizar un programa para una caja de un supermercado que lea un precio desde el teclado y una
cantidad entregada por el cliente (se supone que cantidad >= precio) y obtenga en la pantalla el
numero mnimo de monedas de 1 euro, 50 centimos, 10 centimos y 1 centimo que se deben dar de
cambio. Por ejemplo, si precio es 1.12 euros y cantidad es 5 euros, debe dar como resultado 3
monedas de 1 euro, 1 moneda de 50 centimos, 3 monedas de 10 centimos y 8 monedas de 1
centimo
"""

precio = float(input("Introduzca el precio:"))
cantidad = float(input("Introduzca la cantidad entregada por el cliente:"))

cambio = cantidad - precio

def cambio_monedas(cambio, moneda):
    monedas = (int) (cambio // moneda)
    cambio = cambio % moneda
    return monedas, cambio


cambio *= 100 # cambio a centimos para no perder precision

monedas_1euro, cambio = cambio_monedas(cambio, 100)
monedas_50centimos, cambio = cambio_monedas(cambio, 50)
monedas_10centimos, cambio = cambio_monedas(cambio, 10)
monedas_1centimo, cambio = cambio_monedas(cambio, 1)


print("Monedas de 1 euro:", monedas_1euro)
print("Monedas de 50 centimos:", monedas_50centimos)
print("Monedas de 10 centimos:", monedas_10centimos)
print("Monedas de 1 centimo:", monedas_1centimo)
