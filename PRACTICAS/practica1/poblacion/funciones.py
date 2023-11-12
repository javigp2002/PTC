## Escribe a cadena el formato html
import locale
import os
import csv

import numpy as np
from bs4 import BeautifulSoup

DIRECTORIO_ENTRADAS = 'entradas/'
DIRECTORIO_RESULTADOS = 'resultados/'


#
#     Funciones para escribir en html
#     --------------------------------
#
#     Dado un titulo del html genera el formato html con este nombre
#
def html_start(title):
    html = """ <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>""" + title + """"</title>
    <link rel="stylesheet" href="../entradas/estilo.css">
  </head>
  <body>
"""
    return html


#
#     Funciones para escribir en html
#     --------------------------------
#
#     Genera el formato en cadena para el final del html
#
def html_end():
    html = """ </body> </html> """
    return html


#
#     Funciones para escribir en html
#     --------------------------------
#
#     Genera la página web con el titulo y la body que se le pasa
#     Esta se escribe en el fichero 'file' que se le pasa
#
def write_html(file, title, body):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html_start(title))
        f.write(body)
        f.write(html_end())

## Funciones para el calculo de la poblacion de Variación absoluta y relativa según sus formulas
variacion_absoluta = lambda poblacion, poblacion_anterior: poblacion - poblacion_anterior
variacion_relativa = lambda poblacion, poblacion_anterior: (poblacion - poblacion_anterior) / poblacion_anterior * 100


# Convierte el csv a una cadena con los datos necesarios dado una primera y ultima palabra a buscar
#  file: fichero csv
#   First_word: primera palabra a buscar
#   last_word: ultima palabra a buscar

def csv_to_cleaned_cad(file, first_word, last_word):
    first_file = open(file, "r", encoding="utf8")
    cad = first_file.read()
    first_file.close()

    first = cad.find(first_word)
    last = cad.find(last_word)

    return cad[first:last]


# Crea el fichero csv desde una cadena y devolvemos el nombre del nuevo archivo
def write_cad_to_csv(csv, cad, cabecera=""):
    # modificar la ultima parte del path
    csv_name = csv.split("/")[-1]
    new_csv = csv.replace(csv_name, "new_" + csv_name)

    new_file = open(new_csv, "w", encoding="utf8")

    new_file.write(cabecera + cad)
    new_file.close()
    return new_csv


# Escribe un csv con los datos limpios y devolvemos el nombre del nuevo archivo
def write_cleaned_csv(file, first_word, last_word, cabecera=""):
    cad = csv_to_cleaned_cad(file, first_word, last_word)
    new_file = write_cad_to_csv(file, cad, cabecera)

    return new_file


# Dado un csv genérico de la Junta recoge los años en los que este contiene los datos
def get_years_csv(file):
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


# funcion para recoger un diccionario y devolverlo con los valores que necesitamos
# Dado una cabecera podemos necesitar desagregar información según sus caracteristicas
#       años y caracteres (Total, Hombres, Mujeres)
def clean_dict(chars_to_keep, dict, years_required):
    cleaned_dict = {}
    for key in dict:
        if key and len(key) > 0 and key[0] in chars_to_keep and key[1::] in years_required or key == "Provincia":
            cleaned_dict[key] = dict[key]

    return cleaned_dict


# Dado un diccionario devuelve un array con los nombres de las claves
def get_array_of_dict_keys(dict):
    array_names = []
    for key in dict.keys():
        array_names.append(key)

    return array_names


# funcion para leer el csv limpio y devolver según dada una cabecera, desagregar información según sus caracteristicas
#       años y caracteres (Total, Hombres, Mujeres)
# - elimina el fichero csv limpio
# - Devuelve un array de diccionarios con los datos requeridos
def csv_to_array_dict(file, chars_to_keep, years_required):
    with open(file, encoding='utf-8') as f:
        array_dict = []
        for rec in csv.DictReader(f, delimiter=';'):
            array_dict.append(clean_dict(chars_to_keep, rec, years_required))

    os.remove(file)
    return array_dict


# Devuelve en un diccionario de las comunidades autonomas con un array de todas sus provincias
def dict_autonomies_provinces():
    dict_valores_autonomias = dict_autonomies()

    comunidades_provinces_fich = open(DIRECTORIO_ENTRADAS + 'comunidadAutonoma-Provincia.htm', 'r', encoding="utf8")
    datos = comunidades_provinces_fich.read()

    soup = BeautifulSoup(datos, 'html.parser')
    celdas = soup.find_all('tr')

    # coge los valores de las celdas de 2 en 2
    for celda in celdas:
        temp = celda.get_text().split("\n")
        if temp[1].isnumeric():
            autonomia = temp[1] + " " + temp[2]
            provincia = temp[3] + " " + temp[4]

            temp_add = dict_valores_autonomias[autonomia]
            temp_add.append(provincia)
            dict_valores_autonomias[autonomia] = temp_add

    return dict_valores_autonomias


# En comunidadesAutonomas.htm estan las comunidades autonomas, las cogemos y las metemos en un diccionario
# con un array vacio para meter las provincias posteriormente
def dict_autonomies():
    dict_autonomies = {}
    comunidades_fich = open(DIRECTORIO_ENTRADAS + 'comunidadesAutonomas.htm', 'r', encoding="utf8")
    datos = comunidades_fich.read()

    soup = BeautifulSoup(datos, 'html.parser')
    celdas = soup.find_all('tr')

    # coge los valores de las celdas de 2 en 2
    for celda in celdas:
        temp = celda.get_text().split("\n")
        if temp[1][0].isnumeric():
            autonomy = temp[1] + temp[2]
            autonomy = autonomy.replace(" - ", "-")
            dict_autonomies[autonomy] = []

    return dict_autonomies


# funcion que dada una lista de diccionarios con las autonomias y sus provincias, y numpys con los datos recogidos
# de las provincias.
#       Devuelve un diccionario con cada autonomia y su numpy de la suma de los datos de sus provincias
def provinces_data_to_autonomies_data(province_data, dict_autonomies):
    new_dict_autonomies = {}
    for autonomy in dict_autonomies:
        number_of_data = len(province_data[dict_autonomies[autonomy][0]])
        final_array = np.zeros(number_of_data)

        for province in dict_autonomies[autonomy]:
            final_array = np.add(final_array, province_data[province])

        new_dict_autonomies[autonomy] = final_array
    return new_dict_autonomies


# Función para, dado un array de diccionarios con los datos de las provincias recogidos del csv,
#
#   Devolver un diccionario con cada provincia y sus datos en un numpy
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


# Funcion para, dado un fichero csv, una primera y ultima palabra a buscar, los caracteres a mantener y la cabecera
#   Devolver un diccionario con cada autonomia y sus datos en un numpy
#
# Esta función se utiliza para no repetir codigo en los distintos R
def get_dict_autonomies_with_provinces_data(file, first_word, last_word, chars_to_keep, years_required, cabecera):
    new_file = write_cleaned_csv(file, first_word, last_word, cabecera)
    array_dict = csv_to_array_dict(new_file, chars_to_keep, years_required)

    province_data = save_provinces_data_in_numpy(array_dict)
    return provinces_data_to_autonomies_data(province_data, dict_autonomies_provinces())


# funcion para pasar un float a una cadena con formato de moneda añadiendo los . de los miles y la , de los decimales
#   float: valor a pasar a cadena
#   decimals: numero de decimales a mostrar

def float_to_formated_cad(float, decimals=2):
    locale.setlocale(locale.LC_ALL, '')
    return locale.format_string('%.' + str(decimals) + 'f', float, grouping=True)


# funcion para devolver el nombre de las comunidades autónomas sin el código
def array_comunities_without_code(array_with_codes):
    new_array_without_codes = []
    for autonomy in array_with_codes:
        new_array_without_codes.append(autonomy[2::])

    return new_array_without_codes
