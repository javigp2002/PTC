import locale
import os
import urllib.request

import numpy as np
from bs4 import BeautifulSoup
import certifi
import ssl
from funciones import html_start, html_end, csv_to_cleaned_cad, write_cad_to_csv, get_years_csv, write_cleaned_csv, \
    write_html, DIRECTORIO_FICHEROS, csv_to_array_dict, get_array_of_dict_keys, list_autonomies_provinces, \
    provinces_data_to_autonomies_data, save_provinces_data_in_numpy, float_to_formated_cad
import csv

# Variables globales para la lectura del css en R2
FIRST_WORD = "02 Albacete"
LAST_WORD = "Notas"

CABECERA = ("Provincia;T2017;T2016;T2015;T2014;T2013;T2012;T2011;T2010;H2017;H2016;H2015;H2014;H2013;H2012;H2011"
            ";H2010;M2017;M2016;M2015;M2014;M2013;M2012;M2011;M2010;\n")

YEARS_REQUIRED = ['2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']
CHARS_TO_KEEP = "THM"

SALIDAHTML = "poblacionComAutonomas.html"


def R2(file):
    new_file = write_cleaned_csv(file, FIRST_WORD, LAST_WORD, CABECERA)

    array_dict = csv_to_array_dict(new_file, CHARS_TO_KEEP, YEARS_REQUIRED)
    province_data = save_provinces_data_in_numpy(array_dict)
    list_autonomies = provinces_data_to_autonomies_data(province_data, list_autonomies_provinces())

    cad = cad_list_data_autonomies(list_autonomies)

    tabla = th_table(YEARS_REQUIRED) + cad

    body = tabla + "<img src='imagenes/R3.png' alt='Gráfico de barras de la población por comunidades autónomas'>\n"

    title = "Variación de la población por comunidades autónomas"
    write_html(SALIDAHTML, title, body)



# funcion para las columnas del html
def th_table(years):
    number_of_years = len(years)
    number_of_years_str = str(number_of_years)

    tabla = """<table>\n
                <tr>\n
                </tr>\n
                <tr>\n
                    <th rowspan='2'>CCAA</th> \n
                    <th colspan=" """ + number_of_years_str + """"> Total </th>\n
                    <th colspan=" """ + number_of_years_str + """"> Hombre </th>\n
                    <th colspan=" """ + number_of_years_str + """"> Mujer </th>\n
                </tr>\n
                <tr>\n"""

    for i in range(0, number_of_years * 3):
        tabla += """<th> """ + str(years[i % number_of_years]) + """ </th>\n"""
    tabla += "</tr>\n"

    return tabla




# funcion para leer el csv limpio y escribirlo en el html
def cad_list_data_autonomies(list_autonomies):
    cad = ""
    for autonomy in list_autonomies:
        cad += "<tr>\n<td>" + str(autonomy) + "</td>\n"

        number_of_data = len(list_autonomies[autonomy])

        for i in range(1, number_of_data):
            cad += "<td>" + float_to_formated_cad(list_autonomies[autonomy][i]) + "</td>\n"

        cad += "</tr>\n"

    cad += "</table>\n"

    return cad



# MAIN
file = DIRECTORIO_FICHEROS + "poblacionProvinciasHM2010-17.csv"
R2(file)
