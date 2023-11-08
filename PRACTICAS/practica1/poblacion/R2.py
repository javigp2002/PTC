import locale
import os
import urllib.request

import numpy as np
from bs4 import BeautifulSoup
import certifi
import ssl
from funciones import html_start, html_end, csv_to_cleaned_cad, write_cad_to_csv, get_years_csv, write_cleaned_csv, \
    write_html
import csv

# Variables globales para la lectura del css en R2
FIRST_WORD = "02 Albacete"
LAST_WORD = "Notas"

SALIDAHTML = "poblacionComAutonomas.html"


def R2(file):
    new_file = write_cleaned_csv(file, FIRST_WORD, LAST_WORD)

    years = get_years_csv(file)
    number_of_years = len(years)

    province_data = save_provinces_data(new_file, number_of_years)
    cad = cad_list_data_autonomies(list_autonomies_provinces(), province_data, number_of_years)

    tabla = th_table(years) + cad
    title = "Variación de la población por comunidades autónomas"
    write_html(SALIDAHTML, title, tabla)

    os.remove(new_file)

# Devuelve en un array las tuplas de las comunidades autonomas con cada provincia
def list_autonomies_provinces():
    dict_valores_autonomias = {}

    url = "https://www.ine.es/daco/daco42/codmun/cod_ccaa_provincia.htm"
    datos = urllib.request.urlopen(url).read()  # en utf8
    soup = BeautifulSoup(datos, 'html.parser')
    celdas = soup.find_all('tr')

    # coge los valores de las celdas de 2 en 2
    for celda in celdas:
        temp = celda.get_text().split("\n")
        if (temp[1].isnumeric()):
            autonomia = temp[1] + " " + temp[2]
            provincia = temp[3] + " " + temp[4]

            if autonomia in dict_valores_autonomias:
                temp_add = dict_valores_autonomias[autonomia]
                temp_add.append(provincia)
                dict_valores_autonomias[autonomia] = temp_add
            else:
                dict_valores_autonomias[autonomia] = [provincia]

    return dict_valores_autonomias


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
    tabla +="</tr>\n"

    return tabla


# funcion para leer el csv limpio y escribirlo en el html
def cad_list_data_autonomies(list_autonomies, province_data, years):
    locale.setlocale(locale.LC_ALL, '')
    cad = ""
    for autonomy in list_autonomies:
        cad += "<tr>\n<td>" + str(autonomy) + "</td>\n"

        final_array = np.zeros(years * 3+1)

        for province in list_autonomies[autonomy]:
            final_array = np.add(final_array, province_data[province])

        for i in range(1, years * 3+1):
            cad += "<td>" + locale.format_string('%.2f', final_array[i], grouping=True) + "</td>\n"

        cad += "</tr>\n"

    cad += "</table>\n"

    return cad


# funcion para recopilar valores de las provincias
def save_provinces_data(file, number_years):
    with open(file, encoding='utf-8') as f:
        dict_provinces_data = {}
        for rec in csv.reader(f, delimiter=';'):
            num_valores = number_years * 3 + 1  # Hay que contar el nombre de la provincia
            valores_totales = np.zeros(num_valores)

            for i in range(1, num_valores):
                valores_totales[i] = (rec[i])

            dict_provinces_data[rec[0]] = valores_totales
    return dict_provinces_data


# MAIN
file = "entradas/poblacionProvinciasHM2010-17.csv"
R2(file)
