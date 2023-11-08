## Escribe a cadena el formato html
import os
import csv

DIRECTORIO_FICHEROS='entradas/'
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
def write_cleaned_csv(file, first_word, last_word, cabecera =""):
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