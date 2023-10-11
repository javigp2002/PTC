"""
Realizar un programa que pida un valor X de porcentaje de alcohol de una marca de cerveza y
que según dicho porcentaje calcule cuantos tercios de esa marca de cerveza (333cc) puedo tomar si
no quiero ingerir más de 50 cc de alcohol. Dar el resultado en valor entero.
"""

porcentaje_alcohol = float(input("Introduzca el porcentaje de alcohol:"))

tercios = (int) (50 / (333 * porcentaje_alcohol / 100))

print("Puedes tomar", tercios, "tercios de cerveza")