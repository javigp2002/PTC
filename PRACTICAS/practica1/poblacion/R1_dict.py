"""
R1. Calcular la variación de la población por provincias desde el año 2011 a 2017 en términos absolutos y relativos
 generando la página web 1 (que debe llamarse variacionProvincias.html) que contenga una tabla parecida a la que
 se puede observar en el siguiente ejemplo:
"""

import csv
import os
import numpy as np
from funciones import html_start, html_end, csv_to_cleaned_cad, write_cad_to_csv, get_years_csv

## Funciones para el calculo de la poblacion
variacion_absoluta = lambda poblacion, poblacion_anterior: poblacion - poblacion_anterior
variacion_relativa = lambda poblacion, poblacion_anterior: (poblacion - poblacion_anterior) / poblacion_anterior * 100

# Variables globales para la lectura del css en R1
FIRST_WORD = "Total Nacional"
LAST_WORD = "Notas"

# Variable para conocer los datos que queremos manterner entre (T) totales, (H) hombres y (M) mujeres
CHARS_TO_KEEP = "T"

# Variable cabecera
CABECERA = ("Provincia;T2017;T2016;T2015;T2014;T2013;T2012;T2011;T2010;H2017;H2016;H2015;H2014;H2013;H2012;H2011"
            ";H2010;M2017;M2016;M2015;M2014;M2013;M2012;M2011;M2010;\n")

SALIDAHTML= "variacionProvincias.html"

# funcion para escribir el html con sus datos nuevos
def write_html(file):
    cad = csv_to_cleaned_cad(file, FIRST_WORD, LAST_WORD)
    new_file = write_cad_to_csv(file, cad, CABECERA)

    # cogemos el numero de años que vamos a tener en la tabla
    years = get_years_csv(file)
    number_of_years = len(years) - 1 #-1 por la variación
    number_of_years_str = str(number_of_years)

    # leemos el csv limpio y lo pasamos a un array de diccionarios para luego tener una cadena con los datos en html
    array_dict = csv_to_array_dict(new_file)
    cad = dict_to_cad_html(array_dict)

    with open(SALIDAHTML, 'w', encoding='utf-8') as f:
        f.write(html_start("Variación de la población por provincias"))

        tabla = """<table>\n
            <tr>\n
                <th></th> \n
                <th colspan=" """ + number_of_years_str + """"> Variación absoluta </th>\n
                <th colspan=" """ + number_of_years_str + """"> Variación relativa </th>\n
            </tr>\n
            <tr>\n
                <th> Provincia </th> \n"""

        temp_cad_years = ""
        for i in range(0, number_of_years):
            tabla += """<th> """ + str(years[i]) + """ </th>\n"""
            temp_cad_years += """<th> """ + str(years[i]) + """ </th>\n"""

        tabla += temp_cad_years + "</tr>\n"
        tabla += cad
        tabla += "</table>\n"
        f.write(tabla)
        f.write(html_end())


# funcion para leer el csv limpio y escribirlo en el html
def csv_to_array_dict(file):
    with open(file, encoding='utf-8') as f:
        array_dict = []
        for rec in csv.DictReader(f, delimiter=';'):
            array_dict.append(clean_dict(CHARS_TO_KEEP, rec))

    os.remove(file)
    return array_dict


# funcion para recoger un diccionario y devolverlo con los valores que necesitamos
def clean_dict(chars_to_keep, dict):
    cleaned_dict = {}
    for key in dict:
        if len(key) > 0 and key[0] in chars_to_keep or key == "Provincia":
            cleaned_dict[key] = dict[key]

    return cleaned_dict


# funcion para dado un [] de diccionarios, devolver una cadena con los datos para tabla de variación absoluta y relativa
def dict_to_cad_html(array_dict):
    cad = ""

    # cogemos los "keys" del primer diccionario para saber el orden de las columnas
    if array_dict:
        array_names = get_array_of_dict_keys(array_dict[0])
        print(array_names)
    else:  # no puede imprimir nada si no hay datos
        return cad

    # recorremos el array de diccionarios y vamos escribiendo la cadena
    for actual_dict in array_dict:
        cad += "<tr> <td>" + actual_dict[array_names[0]] + "</td>\n"
        cad_relative = ""

        num_variations = len(array_names) - 1  # -1 para no coger el ultimo elemento que es el total
        for i in range(1, num_variations):
            a = float(actual_dict[array_names[i]])
            b = float(actual_dict[array_names[i + 1]])
            cad += "<td>" + str(round(variacion_absoluta(a, b), 2)) + "</td>\n"
            cad_relative += "<td>" + str(round(variacion_relativa(a, b), 2)) + "</td>\n"

        cad += cad_relative
        cad += "</tr>"
    return cad


def get_array_of_dict_keys(dict):
    array_names = []
    for key in dict.keys():
        array_names.append(key)

    return array_names


# MAIN
file = "entradas/poblacionProvinciasHM2010-17.csv"
write_html(file)
