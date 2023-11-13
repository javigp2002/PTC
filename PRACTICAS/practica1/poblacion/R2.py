"""
R2.
R2. Usando el listado de comunidades autónomas que podemos obtener del fichero
comunidadesAutonomas.html, así como de las provincias de cada comunidad autónoma que podemos obtener de
comunidadAutonoma-Provincia.html y los datos de poblacionProvinciasHM2010-17.csv, hay que generar una
página web 2 (fichero poblacionComAutonomas.html) con una tabla con los valores de población de cada comunidad
autónoma en cada año de 2010 a 2017, indicando también los valores desagregados por sexos (de manera semejante
a como aparece en la siguiente figura). Las celdas deben tener el contenido centrado.
"""

from funciones import write_html, DIRECTORIO_ENTRADAS, float_to_formated_cad, \
    get_dict_autonomies_with_provinces_data, DIRECTORIO_RESULTADOS

# Variables globales para la lectura del css en R2
FIRST_WORD = "02 Albacete"
LAST_WORD = "Notas"

CABECERA = ("Provincia;T2017;T2016;T2015;T2014;T2013;T2012;T2011;T2010;H2017;H2016;H2015;H2014;H2013;H2012;H2011"
            ";H2010;M2017;M2016;M2015;M2014;M2013;M2012;M2011;M2010;\n")

YEARS_REQUIRED = ['2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']
CHARS_TO_KEEP = "THM"

FILE = DIRECTORIO_ENTRADAS + "poblacionProvinciasHM2010-17.csv"
SALIDAHTML = DIRECTORIO_RESULTADOS + "poblacionComAutonomas.html"
DECIMALS_TO_SHOW = 0


def r2():
    dict_autonomies = get_dict_autonomies_with_provinces_data(FILE, FIRST_WORD, LAST_WORD, CHARS_TO_KEEP,
                                                              YEARS_REQUIRED, CABECERA)

    cad = cad_list_data_autonomies(dict_autonomies)

    body = th_table(YEARS_REQUIRED) + cad

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
            cad += "<td>" + float_to_formated_cad(list_autonomies[autonomy][i], DECIMALS_TO_SHOW) + "</td>\n"

        cad += "</tr>\n"

    cad += "</table>\n"

    return cad


if __name__ == "R2":  # Cada vez que lo importe se ejecutará  lo que esté aquí dentro
    print("Importando y ejecutando R2.py")
    r2()

if __name__ == "__main__":  # Si lo ejecuto como fichero principal, se ejecuta lo que hay aquí dentro
    r2()
