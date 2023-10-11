"""
  Realizar un programa que tomando como entrada la radiación solar media por día en Kwh/m2
calcule el número mínimo de paneles solares que se necesitan para producir, al menos, 1000 Kwh
en un mes (30 días) teniendo en cuenta que los paneles solares tienen un 17% de rendimiento y que
son de un tamaño de 1.6 m2.
"""
import math

radiacion_solar = float(input("Introduzca la radiacion solar media por dia en Kwh/m^2:"))

rendimiento_panel = 0.17
tamano_panel = 1.6

kwh_obtenidos = radiacion_solar*tamano_panel*rendimiento_panel
kwh_obtenidos_mes = kwh_obtenidos*30

paneles_minimos = math.ceil(1000 / kwh_obtenidos_mes)

print("Se necesitan", paneles_minimos, "paneles solares para producir al menos 1000 Kwh en un mes")