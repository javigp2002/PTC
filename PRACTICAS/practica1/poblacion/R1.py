"""
R1. Calcular la variación de la población por provincias desde el año 2011 a 2017 en términos absolutos y relativos
 generando la página web 1 (que debe llamarse variacionProvincias.html) que contenga una tabla parecida a la que
 se puede observar en el siguiente ejemplo:
"""

import csv
import os
import numpy as np
from funciones import html_start, html_end

## Funciones para el calculo de la poblacion
variacion_absoluta = lambda poblacion, poblacion_anterior: poblacion - poblacion_anterior
variacion_relativa = lambda poblacion, poblacion_anterior: (poblacion - poblacion_anterior) / poblacion_anterior * 100

# Variables globales para la lectura del css en R1
FIRST_WORD = "Total Nacional"
LAST_WORD = "Notas"


# funcion para escribir el html con sus datos nuevos
def write_html(file):
    cad = csv_to_cleaned_cad(file, FIRST_WORD, LAST_WORD)
    years = get_years(file)
    new_file = write_cad_to_csv(file, cad)

    number_of_years = len(years) - 1
    number_of_years_str = str(number_of_years)
    cad = read_final_csv(new_file, years)

    with open("salida.html", 'w', encoding='utf-8') as f:
        f.write(html_start("Variación de la población por provincias"))

        tabla = """<table>\n
            <tr>\n
                <th></th> \n
                <th colspan=" """ + number_of_years_str + """"> Variación absoluta </th>\n
                <th colspan=" """ + number_of_years_str + """"> Variación relativa </th>\n
            </tr>\n
            <tr>\n
                <th> Provincia </th> \n"""

        for i in range(0, number_of_years):
            tabla += """<th> """ + str(years[i]) + """ </th>\n"""
        for i in range(0, number_of_years):
            tabla += """<th> """ + str(years[i]) + """ </th>\n"""

        tabla += "</tr>\n"
        tabla += cad
        tabla += "</table>\n"
        f.write(tabla)
        f.write(html_end())


# funcion para leer el csv limpio y escribirlo en el html
def read_final_csv(file, years):
    number_years = (len(years) - 1)

    with open(file, encoding='utf-8') as f:
        cad = ""
        for rec in csv.reader(f, delimiter=';'):
            cad += "<tr>"
            cad += "<td>" + str(rec[0]) + "</td>"
            for i in range(0, number_years):
                cad += "<td>" + str(round(variacion_absoluta(float(rec[i + 1]), float(rec[i + 2])), 2)) + "</td>\n"

            for i in range(0, number_years):
                cad += "<td>" + str(round(variacion_relativa(float(rec[i + 1]), float(rec[i + 2])), 2)) + "</td>\n"
            cad += "</tr>"

    os.remove(file)
    return cad


# Convierte el csv a una cadena con los datos necesarios dado una primera y ultima palabra a buscar
def csv_to_cleaned_cad(file, first_word, last_word):
    first_file = open(file, "r", encoding="utf8")
    cad = first_file.read()
    first_file.close()

    first = cad.find(first_word)
    last = cad.find(last_word)

    return cad[first:last]


# Escribe una cadena en un archivo csv y devolvemos el nombre del nuevo archivo
def write_cad_to_csv(csv, cad):
    # modificar la ultima parte del path
    csv_name = csv.split("/")[-1]
    new_csv = csv.replace(csv_name, "new_" + csv_name)

    new_file = open(new_csv, "w", encoding="utf8")
    new_file.write(cad)
    new_file.close()
    return new_csv


# Dado un csv genérico recoge los años en los que este contiene los datos
def get_years(file):
    years = []
    with open(file, encoding='utf-8') as f:
        data = csv.reader(f, delimiter=';')
        for reg in data:
            if len(reg) > 1 and reg[1].isnumeric():
                for i in range(1, len(reg)):
                    years.append(int(reg[i]))
                    if i != 1 and years[0] == int(reg[i]):
                        years.pop()  # ultima almacenada = primera
                        break

                return years

    return years


# MAIN
file = "entradas/poblacionProvinciasHM2010-17.csv"
write_html(file)
