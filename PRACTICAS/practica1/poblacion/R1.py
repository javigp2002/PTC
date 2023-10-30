"""
R1. Calcular la variación de la población por provincias desde el año 2011 a 2017 en términos absolutos y relativos
 generando la página web 1 (que debe llamarse variacionProvincias.html) que contenga una tabla parecida a la que
 se puede observar en el siguiente ejemplo:
"""

import csv
import os
import numpy as np

VARIACION_ABSOLUTA = lambda poblacion, poblacion_anterior: poblacion - poblacion_anterior
VARIACION_RELATIVA = lambda poblacion, poblacion_anterior: (poblacion - poblacion_anterior) / poblacion_anterior * 100
def html_start(title):
    html = """ <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>""" + title + """"</title>
    <link rel="stylesheet" href="./ayudas/estilo.css">
  </head>
  <body>
"""
    return html


def html_end():
    html = """ </body> </html> """
    return html


# funcion para leer del csv suministrado

FIRST_WORD = "Total Nacional"
LAST_WORD = "Notas"



# funcion para escribir el csv en html
def write_html(file):
    cad = clean_csv(file, FIRST_WORD, LAST_WORD)
    years = get_years(file)
    new_file = write_cleaned_csv(file, cad)

    number_of_years = str(len(years) - 1)
    cad = read_final_csv("new_" + file, years)


    with open("salida.html", 'w', encoding='utf-8') as f:
        f.write(html_start("Variación de la población por provincias"))

        tabla = """<table>\n
            <tr>\n
                <th></th> \n
                <th colspan=" """ + number_of_years + """"> Variación absoluta </th>\n
                <th colspan=" """ + number_of_years + """"> Variación relativa </th>\n
            </tr>\n
            <tr>\n
                <th> Provincia </th> \n"""

        for i in range(0, len(years) - 1):
            tabla += """<th> """ + str(years[i]) + """ </th>\n"""
        for i in range(0, len(years) - 1):
            tabla += """<th> """ + str(years[i]) + """ </th>\n"""

        tabla += "</tr>\n"
        tabla += cad
        tabla += "</table>\n"
        f.write(tabla)
        f.write(html_end())


def read_final_csv(file, years):
    number_years = (len(years) - 1)

    with open(file, encoding='utf-8') as f:
        cad = ""
        for rec in csv.reader(f, delimiter=';'):
            cad += "<tr>"
            cad += "<td>" + str(rec[0]) + "</td>"
            for i in range(0,number_years):
                cad += "<td>" + str(round(VARIACION_ABSOLUTA(float(rec[i+1]), float(rec[i + 2])), 2)) + "</td>\n"

            for i in range(0, number_years):
                cad += "<td>" + str(round(VARIACION_RELATIVA(float(rec[i+1]), float(rec[i + 2])), 2)) + "</td>\n"
            cad += "</tr>"

    return cad


def clean_csv(file, first_word, last_word):
    first_file = open(file, "r", encoding="utf8")
    cad = first_file.read()
    first_file.close()

    first = cad.find(first_word)
    last = cad.find(last_word)

    return cad[first:last]


def write_cleaned_csv(file, cad):
    new_file = open("new_" + file, "w", encoding="utf8")
    new_file.write(cad)
    new_file.close()
    return new_file


def get_years(file):
    years = []
    with open(file, encoding='utf-8') as f:
        data = csv.reader(f, delimiter=';')
        for reg in data:
            if len(reg) > 1 and reg[1].isnumeric():
                for i in range(1, len(reg)):
                    years.append(int(reg[i]))
                    if i != 1 and years[0] == int(reg[i]):
                        years.pop() # ultima almacenada = primera
                        break

                return years

    return years



file = "poblacionProvinciasHM2010-17.csv"
write_html(file)

