import locale
import matplotlib.pyplot as plt

import numpy as np
from bs4 import BeautifulSoup
import certifi
import ssl
from funciones import html_start, html_end, csv_to_cleaned_cad, write_cad_to_csv, get_years_csv, write_cleaned_csv, \
    write_html, DIRECTORIO_FICHEROS, csv_to_array_dict, get_array_of_dict_keys
import csv

# Variables globales para la lectura del css en R2
FIRST_WORD = "02 Albacete"
LAST_WORD = "Notas"

CABECERA = ("Provincia;T2017;T2016;T2015;T2014;T2013;T2012;T2011;T2010;H2017;H2016;H2015;H2014;H2013;H2012;H2011"
            ";H2010;M2017;M2016;M2015;M2014;M2013;M2012;M2011;M2010;\n")

YEARS_REQUIRED = ['2017']
CHARS_TO_KEEP = "HM"

SALIDAHTML = "poblacionComAutonomas.html"


def r3(file):
    new_file = write_cleaned_csv(file, FIRST_WORD, LAST_WORD, CABECERA)

    array_dict = csv_to_array_dict(new_file, CHARS_TO_KEEP, YEARS_REQUIRED)

    province_data = save_provinces_data_in_numpy(array_dict)
    dict_autonomies = provinces_data_to_autonomies_data(province_data, list_autonomies_provinces())

    # pinta un grafico de barras con los datos de las autonomias

    etiquetas = get_array_of_dict_keys(dict_autonomies)

    men = []
    woman = []
    for autonomy in dict_autonomies:
        men.append(dict_autonomies[autonomy][1])
        woman.append(dict_autonomies[autonomy][2])


    co = np.arange(len(etiquetas))
    an = 0.35

    fig, ax = plt.subplots()
    ax.bar(co - an/2, men, an, label='Hombres')
    ax.bar(co + an/2, woman, an, label='Mujeres')

    ax.set_title('Población por comunidades autónomas')
    ax.set_ylabel('Población')
    ax.set_xlabel('Comunidades autónomas')
    ax.set_xticks(co)
    ax.set_xticklabels(etiquetas)
    fig.autofmt_xdate(rotation=45)
    plt.savefig('foo.png')

# Devuelve en un array las tuplas de las comunidades autonomas con cada provincia
def list_autonomies_provinces():
    dict_valores_autonomias = {}

    # url = "https://www.ine.es/daco/daco42/codmun/cod_ccaa_provincia.htm"
    # datos = urllib.request.urlopen(url).read()  # en utf8

    comunidadesFich = open(DIRECTORIO_FICHEROS + 'comunidadAutonoma-Provincia.htm', 'r', encoding="utf8")
    datos = comunidadesFich.read()

    soup = BeautifulSoup(datos, 'html.parser')
    celdas = soup.find_all('tr')

    # coge los valores de las celdas de 2 en 2
    for celda in celdas:
        temp = celda.get_text().split("\n")
        if temp[1].isnumeric():
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
    tabla += "</tr>\n"

    return tabla


# funcion que dada una lista de diccionarios con las autonomias y sus provincias, y numpys con los datos de las provincias
# devuelve la suma de esos datos en un numpy por autonomia
def provinces_data_to_autonomies_data(province_data, list_autonomies):
    new_list_autonomies = {}
    for autonomy in list_autonomies:
        number_of_data = len(province_data[list_autonomies[autonomy][0]])
        final_array = np.zeros(number_of_data)

        for province in list_autonomies[autonomy]:
            final_array = np.add(final_array, province_data[province])

        new_list_autonomies[autonomy] = final_array
    return new_list_autonomies


# funcion para leer el csv limpio y escribirlo en el html
def cad_list_data_autonomies(list_autonomies):
    locale.setlocale(locale.LC_ALL, '')
    cad = ""
    for autonomy in list_autonomies:
        cad += "<tr>\n<td>" + str(autonomy) + "</td>\n"

        number_of_data = len(list_autonomies[autonomy])

        for i in range(1, number_of_data):
            cad += "<td>" + locale.format_string('%.2f', list_autonomies[autonomy][i], grouping=True) + "</td>\n"

        cad += "</tr>\n"

    cad += "</table>\n"

    return cad


# funcion para recopilar valores de las provincias
def save_provinces_data_in_numpy(array_dict):
    dict_provinces_data = {}

    # cogemos los "keys" del primer diccionario para saber el orden de las columnas
    if array_dict:
        array_names = get_array_of_dict_keys(array_dict[0])
    else:
        raise ValueError("No hay datos")

    for actual_dict in array_dict:
        num_valores = len(array_names)
        valores_totales = np.zeros(num_valores)

        for i in range(1, num_valores):
            valores_totales[i] = (actual_dict[array_names[i]])

        dict_provinces_data[actual_dict[array_names[0]]] = valores_totales

    return dict_provinces_data

# MAIN
file = DIRECTORIO_FICHEROS + "poblacionProvinciasHM2010-17.csv"
r3(file)
