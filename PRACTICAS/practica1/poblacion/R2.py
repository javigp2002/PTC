from funciones import write_cleaned_csv, \
    write_html, DIRECTORIO_FICHEROS, csv_to_array_dict, dict_autonomies_provinces, \
    provinces_data_to_autonomies_data, save_provinces_data_in_numpy, float_to_formated_cad, \
    get_dict_autonomies_with_provinces_data

# Variables globales para la lectura del css en R2
FIRST_WORD = "02 Albacete"
LAST_WORD = "Notas"

CABECERA = ("Provincia;T2017;T2016;T2015;T2014;T2013;T2012;T2011;T2010;H2017;H2016;H2015;H2014;H2013;H2012;H2011"
            ";H2010;M2017;M2016;M2015;M2014;M2013;M2012;M2011;M2010;\n")

YEARS_REQUIRED = ['2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']
CHARS_TO_KEEP = "THM"

SALIDAHTML = "poblacionComAutonomas.html"


def R2(file):
    dict_autonomies = get_dict_autonomies_with_provinces_data(file, FIRST_WORD, LAST_WORD, CHARS_TO_KEEP,
                                                              YEARS_REQUIRED, CABECERA)

    cad = cad_list_data_autonomies(dict_autonomies)

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
            cad += "<td>" + float_to_formated_cad(list_autonomies[autonomy][i], 0) + "</td>\n"

        cad += "</tr>\n"

    cad += "</table>\n"

    return cad


# MAIN
file = DIRECTORIO_FICHEROS + "poblacionProvinciasHM2010-17.csv"
R2(file)
