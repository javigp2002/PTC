"""
R4. Generar una página web 3 (fichero variacionComAutonomas.html) con una tabla con la variación
de población por comunidades autónomas desde el año 2011 a 2017, indicando variación absoluta,
relativa y desagregando dicha información por sexos, es decir, variación absoluta (hombres, mujeres)
y relativa (hombres, mujeres). Para los cálculos, hay que actuar de manera semejante que en el apartado R1.
"""

from funciones import write_cleaned_csv, \
    write_html, DIRECTORIO_ENTRADAS, get_array_of_dict_keys, csv_to_array_dict, float_to_formated_cad, \
    DIRECTORIO_RESULTADOS, get_dict_autonomies_with_provinces_data, variacion_absoluta, variacion_relativa

# Variables globales para la lectura del css en R1
FIRST_WORD = "Total Nacional"
LAST_WORD = "Notas"

# Variable para conocer los datos que queremos manterner entre (T) totales, (H) hombres y (M) mujeres
CHARS_TO_KEEP = "HM"

# Variable cabecera
CABECERA = ("Provincia;T2017;T2016;T2015;T2014;T2013;T2012;T2011;T2010;H2017;H2016;H2015;H2014;H2013;H2012;H2011"
            ";H2010;M2017;M2016;M2015;M2014;M2013;M2012;M2011;M2010;\n")

YEARS_REQUIRED = ['2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']

SALIDAHTML = DIRECTORIO_RESULTADOS + "variacionComAutonomas.html"

DECIMALS_TO_SHOW = 2


def r4(file):
    new_file = write_cleaned_csv(file, FIRST_WORD, LAST_WORD, CABECERA)
    dict_comunities = get_dict_autonomies_with_provinces_data(new_file, FIRST_WORD, LAST_WORD, CHARS_TO_KEEP,
                                                              YEARS_REQUIRED, CABECERA)

    title = "Variaciones de la comunidades por sexos"

    tabla = th_table() + dict_to_cad_html(dict_comunities)

    write_html(SALIDAHTML, title, tabla)


# funcion para las columnas del html
def th_table():
    years = YEARS_REQUIRED

    number_of_years = len(years)
    number_of_years_str = str(number_of_years)
    number_of_variations = number_of_years - 1
    variatons_colspan = (len(years) - 1) * 2
    variatons_colspan_str = str(variatons_colspan)

    tabla = """<table>\n
                    <tr>\n
                    </tr>\n
                    <tr>\n
                        <th rowspan='3'>CCAA</th> \n
                        <th colspan=" """ + variatons_colspan_str + """"> Variación Absoluta </th>\n
                        <th colspan=" """ + variatons_colspan_str + """"> Variación Relativa </th>\n
                    </tr>\n
                    <tr>\n
                        <th colspan=" """ + str(number_of_variations) + """"> Hombres </th>\n
                        <th colspan=" """ + str(number_of_variations) + """"> Mujeres </th>\n
                        <th colspan=" """ + str(number_of_variations) + """"> Hombres </th>\n
                        <th colspan=" """ + str(number_of_variations) + """"> Mujeres </th>\n
                    <tr>\n"""

    for i in range(0, (number_of_variations * 4)):
        tabla += """<th> """ + str(years[i % number_of_variations]) + """ </th>\n"""
    tabla += "</tr>\n"

    return tabla


# funcion para dado un [] de diccionarios, devolver una cadena con los datos para tabla de variación absoluta y relativa
def dict_to_cad_html(dict):
    cad = ""

    # cogemos los "keys" del primer diccionario para saber el orden de las columnas
    if dict:
        array_names = get_array_of_dict_keys(dict)
    else:  # no puede imprimir nada si no hay datos
        return cad

    num_years = int(dict[array_names[0]].size)
    for autonomy in range(0, len(array_names)):
        cad += "<tr> <td>" + array_names[autonomy] + "</td>\n"

        cad_absolute = ""
        cad_relative = ""

        cad_absolute, cad_relative = cad_absolute_relative_autonomy(1, num_years // 2, dict, array_names,
                                                                    autonomy, cad_absolute, cad_relative)

        cad_absolute, cad_relative = cad_absolute_relative_autonomy(num_years // 2 + 1, num_years - 1, dict,
                                                                    array_names,
                                                                    autonomy, cad_absolute, cad_relative)

        cad += cad_absolute + cad_relative
        cad += "</tr>"
    cad += "</table>\n"
    return cad


# Dados:
#  - start: inicio para recorrer el numpy de la autonomia
#  - end: final para recorrer el numpy de la autonomia
#  - dict: diccionario con los datos de las autonomias
#  - array_names: array con los nombres de las autonomias
#  - autonomy: autonomia que se esta recorriendo
#  - cad_absolute: cadena con los datos de la variacion absoluta
#  - cad_relative: cadena con los datos de la variacion relativa
#
# Devuelve:
#  - cad_absolute: cadena con los nuevos y antiguos datos de la variacion absoluta
#  - cad_relative: cadena con los nuevos y antiguos datos de la variacion relativa
def cad_absolute_relative_autonomy(start, end, dict, array_names, autonomy, cad_absolute, cad_relative):
    for i in range(start, end):
        a = float(dict[array_names[autonomy]][i])
        b = float(dict[array_names[autonomy]][i + 1])

        cad_absolute += "<td>" + float_to_formated_cad((variacion_absoluta(a, b), DECIMALS_TO_SHOW)) + "</td>\n"
        cad_relative += ("<td>" + float_to_formated_cad(round(variacion_relativa(a, b), DECIMALS_TO_SHOW)) + "</td>\n")

    return cad_absolute, cad_relative


# MAIN
file = DIRECTORIO_ENTRADAS + "poblacionProvinciasHM2010-17.csv"
r4(file)
