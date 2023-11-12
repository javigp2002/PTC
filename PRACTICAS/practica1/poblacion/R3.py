import locale
import matplotlib.pyplot as plt

import numpy as np
from bs4 import BeautifulSoup
import certifi
import ssl
from funciones import html_start, html_end, csv_to_cleaned_cad, write_cad_to_csv, get_years_csv, write_cleaned_csv, \
    write_html, DIRECTORIO_FICHEROS, csv_to_array_dict, get_array_of_dict_keys, save_provinces_data_in_numpy, \
    provinces_data_to_autonomies_data, dict_autonomies_provinces, get_dict_autonomies_with_provinces_data
import csv

# Variables globales para la lectura del css en R3
FIRST_WORD = "02 Albacete"
LAST_WORD = "Notas"
CABECERA = ("Provincia;T2017;T2016;T2015;T2014;T2013;T2012;T2011;T2010;H2017;H2016;H2015;H2014;H2013;H2012;H2011"
            ";H2010;M2017;M2016;M2015;M2014;M2013;M2012;M2011;M2010;\n")

YEARS_REQUIRED = ['2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']
CHARS_TO_KEEP = "T"

# Variables globales para el gráfico de R3
YEARS_POBLATION_GRAPH = ['2017']
CHAR_TO_KEEP_GRAPH = "HM"
NUMBER_AUTONOMIES = 10

# Variable directorio
DIRECTORIO_IMAGENES = "imagenes/"

SALIDAHTML = "poblacionComAutonomas.html"

FILE_TO_READ = DIRECTORIO_FICHEROS + "poblacionProvinciasHM2010-17.csv"


def r3():
    dt = np.dtype([('mean', np.float64), ('name', np.unicode_, 40)])
    array_autonomies_name_sorted = numpy_autonomies_array_sort_by_mean(dt, NUMBER_AUTONOMIES)

    dict_autonomies_graph = get_dict_autonomies_with_provinces_data(FILE_TO_READ, FIRST_WORD, LAST_WORD,
                                                                    CHAR_TO_KEEP_GRAPH, YEARS_POBLATION_GRAPH, CABECERA)

    etiquetas = array_autonomies_name_sorted

    men = []
    woman = []
    for autonomy in array_autonomies_name_sorted:
        men.append(dict_autonomies_graph[autonomy][1])
        woman.append(dict_autonomies_graph[autonomy][2])

    co = np.arange(len(etiquetas))
    an = 0.35

    fig, axes = plt.subplots()

    #Barras que se ponen
    axes.bar(co - an / 2, men, an, label='Hombres')
    axes.bar(co + an / 2, woman, an, label='Mujeres')

    axes.set_title('Población por comunidades autónomas')
    axes.set_ylabel('Población')
    axes.set_xlabel('Comunidades autónomas')
    axes.set_xticks(co)
    axes.set_xticklabels(etiquetas)
    fig.autofmt_xdate(rotation=45)
    plt.savefig(DIRECTORIO_IMAGENES + 'R3.png', bbox_inches='tight')


# Dado el fichero de csv con su cabecera y limpio de datos innecesarios, devuelve el array con el nombre de las comunidades
# autonomas según la media de población
def numpy_autonomies_array_sort_by_mean(dt, number_of_autonomies):
    dict_autonomies = get_dict_autonomies_with_provinces_data(FILE_TO_READ, FIRST_WORD, LAST_WORD, CHARS_TO_KEEP,
                                                              YEARS_REQUIRED, CABECERA)

    array_top_provinces_poblation_mean = np.array([], dtype=dt)

    for autonomy in dict_autonomies:
        array_top_provinces_poblation_mean = np.append(array_top_provinces_poblation_mean,
                                                       np.array([(dict_autonomies[autonomy].mean(), autonomy)],
                                                                dtype=dt))

    # print(array_top_provinces_poblation_mean)
    array_sorted = np.sort(array_top_provinces_poblation_mean, order='mean')[::-1]
    # coger solo los valores 'name' de las 10 primeras autonomias
    array_sorted = array_sorted[:number_of_autonomies]['name']
    return array_sorted


# funcion para las columnas del html

# fu
# MAIN
r3()
