import locale
import os
import urllib.request
from bs4 import BeautifulSoup
import certifi
import ssl
from funciones import html_start, html_end, csv_to_cleaned_cad, write_cad_to_csv, get_years
import csv


# Variables globales para la lectura del css en R1
FIRST_WORD = "02 Albacete"
LAST_WORD = "Notas"

# Devuelve en un array las tuplas de las comunidades autonomas con cada provincia
def list_autonomies_provinces():
    # listaValores={}
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

def write_html(file):
    cad = csv_to_cleaned_cad(file, FIRST_WORD, LAST_WORD)
    years = get_years(file)
    new_file = write_cad_to_csv(file, cad)
    province_data = save_provinces_data(new_file, len(years))
    print(province_data)

    number_of_years = len(years)
    number_of_years_str = str(number_of_years)
    cad = cad_list_data_autonomies(list_autonomies_provinces(), province_data, number_of_years)

    with open("salida.html", 'w', encoding='utf-8') as f:
        f.write(html_start("Población con autonomias y provincias"))

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

        for i in range(0, number_of_years*3):
            tabla += """<th> """ + str(years[i%number_of_years]) + """ </th>\n"""


        tabla += "</tr>\n"
        tabla += cad
        tabla += "</table>\n"
        f.write(tabla)
        f.write(html_end())

    os.remove(new_file)


# funcion para leer el csv limpio y escribirlo en el html
def cad_list_data_autonomies(list_autonomies, province_data , years):
    locale.setlocale(locale.LC_ALL, '')
    cad = ""
    for autonomy in list_autonomies:
        cad += "<tr>\n<td>" + str(autonomy) + "</td>\n"
        for i in range (0, years*3):
            poblation_autonomy = 0
            for province in list_autonomies[autonomy]:
                poblation_autonomy += float(province_data[province][i])

            cad += "<td>" + locale.format_string('%.2f', poblation_autonomy, grouping=True) + "</td>\n"

        cad += "</tr>\n"

    return cad



# funcion para recopilar valores de las provincias
def save_provinces_data(file, number_years):
    with open(file, encoding='utf-8') as f:
        dict_provinces_data = {}
        for rec in csv.reader(f, delimiter=';'):
            valores_totales = []
            num_valores = number_years*3 + 1 #Hay que contar el nombre de la provincia

            for i in range(1, num_valores):
                valores_totales.append(rec[i])
            dict_provinces_data[rec[0]] = valores_totales
    return dict_provinces_data

# MAIN
file = "entradas/poblacionProvinciasHM2010-17.csv"
write_html(file)




