"""
# Calcular precio de un vehículo suponiendo que tenemos que pedir como datos de entrada los
siguientes: precio bruto del vehículo, porcentaje de ganancia del vendedor, IVA a aplicar. El precio
base se calcula incrementando el precio bruto con el porcentaje de ganancia. El precio final será el
precio base incrementado con el porcentaje de IVA

"""


precio_bruto = float(input("Precio bruto del vehículo:"))
porcentaje_ganancia = float(input("Introduzca el porcentaje de ganancia:"))
IVA = float(input("Introduzca el IVA:"))

precio_base = precio_bruto * (1 + porcentaje_ganancia / 100)
precio_final = precio_base * (1 + IVA / 100)

print("Precio final del vehiculo: ", round(precio_final, 3))