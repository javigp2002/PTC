## Escribe a cadena el formato html
import locale
import os
import csv

import numpy as np
from bs4 import BeautifulSoup

DIRECTORIO_FICHEROS = 'entradas/'


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


# Escribe a cadena el formato final del html
def html_end():
    html = """ </body> </html> """
    return html


def write_html(file, title, cad):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html_start(title))
        f.write(cad)
        f.write(html_end())


# Convierte el csv a una cadena con los datos necesarios dado una primera y ultima palabra a buscar
def csv_to_cleaned_cad(file, first_word, last_word):
    first_file = open(file, "r", encoding="utf8")
    cad = first_file.read()
    first_file.close()

    first = cad.find(first_word)
    last = cad.find(last_word)

    return cad[first:last]


# Escribe un csv con los datos limpios y devolvemos el nombre del nuevo archivo
def write_cleaned_csv(file, first_word, last_word, cabecera=""):
    cad = csv_to_cleaned_cad(file, first_word, last_word)
    new_file = write_cad_to_csv(file, cad, cabecera)

    return new_file


# Escribe una cadena en un archivo csv y devolvemos el nombre del nuevo archivo
def write_cad_to_csv(csv, cad, cabecera=""):
    # modificar la ultima parte del path
    csv_name = csv.split("/")[-1]
    new_csv = csv.replace(csv_name, "new_" + csv_name)

    new_file = open(new_csv, "w", encoding="utf8")

    new_file.write(cabecera + cad)
    new_file.close()
    return new_csv


# Dado un csv genérico recoge los años en los que este contiene los datos
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
def clean_dict(chars_to_keep, dict, years_required):
    cleaned_dict = {}
    for key in dict:
        if key and len(key) > 0 and key[0] in chars_to_keep and key[1::] in years_required or key == "Provincia":
            cleaned_dict[key] = dict[key]

    return cleaned_dict


def get_array_of_dict_keys(dict):
    array_names = []
    for key in dict.keys():
        array_names.append(key)

    return array_names


# funcion para leer el csv limpio y escribirlo en el html
def csv_to_array_dict(file, chars_to_keep, years_required):
    with open(file, encoding='utf-8') as f:
        array_dict = []
        for rec in csv.DictReader(f, delimiter=';'):
            array_dict.append(clean_dict(chars_to_keep, rec, years_required))

    os.remove(file)
    return array_dict


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


# funcion para recompile valores de las provincias
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


def get_dict_autonomies_with_provinces_data(file, first_word, last_word, chars_to_keep, years_required, cabecera):
    new_file = write_cleaned_csv(file, first_word, last_word, cabecera)
    array_dict = csv_to_array_dict(new_file, chars_to_keep, years_required)

    province_data = save_provinces_data_in_numpy(array_dict)
    return provinces_data_to_autonomies_data(province_data, list_autonomies_provinces())

def float_to_formated_cad(float):
    locale.setlocale(locale.LC_ALL, '')
    return locale.format_string('%.2f', float, grouping=True)
