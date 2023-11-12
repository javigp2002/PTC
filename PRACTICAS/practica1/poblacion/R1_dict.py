"""
R1. Calcular la variación de la población por provincias desde el año 2011 a 2017 en términos absolutos y relativos
 generando la página web 1 (que debe llamarse variacionProvincias.html) que contenga una tabla parecida a la que
 se puede observar en el siguiente ejemplo:
"""

from funciones import write_cleaned_csv, \
    write_html, DIRECTORIO_FICHEROS, get_array_of_dict_keys, csv_to_array_dict, float_to_formated_cad

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

YEARS_REQUIRED = ['2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']

SALIDAHTML = "variacionProvincias.html"

"""
Función
"""


def r1(file):
    new_file = write_cleaned_csv(file, FIRST_WORD, LAST_WORD, CABECERA)

    # leemos el csv limpio y lo pasamos a un array de diccionarios para luego tener una cadena con los datos en html
    array_dict = csv_to_array_dict(new_file, CHARS_TO_KEEP, YEARS_REQUIRED)
    cad = dict_to_cad_html(array_dict)

    title = "Variación de la población por provincias"
    tabla = th_table() + cad

    write_html(SALIDAHTML, title, tabla)


# funcion para las columnas del html
def th_table():
    years = YEARS_REQUIRED
    number_of_years = len(years) - 1  # -1 para no coger el ultimo elemento que es el total
    number_of_years_str = str(number_of_years)

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

    return tabla


# funcion para dado un [] de diccionarios, devolver una cadena con los datos para tabla de variación absoluta y relativa
def dict_to_cad_html(array_dict):
    cad = ""

    # cogemos los "keys" del primer diccionario para saber el orden de las columnas
    if array_dict:
        array_names = get_array_of_dict_keys(array_dict[0])
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
            cad += "<td>" + float_to_formated_cad((variacion_absoluta(a, b), 2)) + "</td>\n"
            cad_relative += ("<td>" + float_to_formated_cad(round(variacion_relativa(a, b), 2)) + "</td>\n")

        cad += cad_relative
        cad += "</tr>"
    cad += "</table>\n"
    return cad


# MAIN
file = DIRECTORIO_FICHEROS + "poblacionProvinciasHM2010-17.csv"
r1(file)
