"""
R3.
R3. Usando Matplotlib, para las 10 comunidades con más población media de 2010 a 2017, generar un gráfico de columnas
que indique la población de hombres y mujeres en el año 2017, salvar el gráfico a fichero e incorporarlo a la
página web 2 del punto R2.
"""

import matplotlib.pyplot as plt
import numpy as np

from funciones import DIRECTORIO_ENTRADAS, array_comunities_without_code, \
    obtener_etiqueta_array_dict_for_graph, DIRECTORIO_RESULTADOS, \
    include_graph_in_html, DIRECTORIO_IMAGENES

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

SALIDAHTML = DIRECTORIO_RESULTADOS + "poblacionComAutonomas.html"

FILE_TO_READ = DIRECTORIO_ENTRADAS + "poblacionProvinciasHM2010-17.csv"


def r3():
    array_autonomies_name_sorted, dict_autonomies_graph = obtener_etiqueta_array_dict_for_graph(FILE_TO_READ,
                                                                                                FIRST_WORD, LAST_WORD,
                                                                                                CHARS_TO_KEEP,
                                                                                                CHAR_TO_KEEP_GRAPH,
                                                                                                YEARS_REQUIRED,
                                                                                                YEARS_POBLATION_GRAPH,
                                                                                                CABECERA,
                                                                                                NUMBER_AUTONOMIES)
    etiquetas = array_autonomies_name_sorted

    men = []
    woman = []
    for autonomy in array_autonomies_name_sorted:
        men.append(dict_autonomies_graph[autonomy][1])
        woman.append(dict_autonomies_graph[autonomy][2])

    directorio_archivo = save_bar_graph(etiquetas, men, woman)
    include_graph_in_html(SALIDAHTML, "../" + directorio_archivo, "Grafico de barras de la  media de "
                                                                  "población total")


# funcion que realiza el gráfico de barras de la población media por comunidades autónomas
# Devuelve la ubicación png del gráfico
def save_bar_graph(etiquette, men, woman):
    co = np.arange(len(etiquette))
    an = 0.35

    fig, axes = plt.subplots()

    # Barras que se ponen
    axes.bar(co - an / 2, men, an, label='Hombres')
    axes.bar(co + an / 2, woman, an, label='Mujeres')

    axes.set_title('Población por comunidades autónomas')
    plt.legend(["Hombres", "Mujeres"])
    axes.set_ylabel('Población')
    axes.set_xlabel('Comunidades autónomas')
    axes.set_xticks(co)
    axes.set_xticklabels(array_comunities_without_code(etiquette))
    fig.autofmt_xdate(rotation=45)

    directorio_archivo = DIRECTORIO_IMAGENES + 'R3.png'
    plt.savefig(directorio_archivo, bbox_inches='tight')

    return directorio_archivo


if __name__ == "R3":  # Cada vez que lo importe se ejecutará  lo que esté aquí dentro
    print("Importando y ejecutando R3.py")
    r3()

if __name__ == "__main__":  # Si lo ejecuto como fichero principal, se ejecuta lo que hay aquí dentro
    r3()
