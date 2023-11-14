"""
R5. Usando Matplotlib, para las 10 comunidades elegidas en el punto R3 generar un
gráfico de líneas que refleje la evolución de la población total de cada comunidad
autónoma desde el año 2010 a 2017, salvar el gráfico a fichero e incorporarlo a la
página web 3 del punto R4.

"""

import matplotlib.pyplot as plt
import numpy as np

from funciones import DIRECTORIO_ENTRADAS, get_dict_autonomies_with_provinces_data, array_comunities_without_code, \
    numpy_autonomies_array_sort_by_mean, obtener_etiqueta_array_dict_for_graph, include_graph_in_html, \
    DIRECTORIO_RESULTADOS, DIRECTORIO_IMAGENES

# Variables globales para la lectura del css en R3
FIRST_WORD = "02 Albacete"
LAST_WORD = "Notas"
CABECERA = ("Provincia;T2017;T2016;T2015;T2014;T2013;T2012;T2011;T2010;H2017;H2016;H2015;H2014;H2013;H2012;H2011"
            ";H2010;M2017;M2016;M2015;M2014;M2013;M2012;M2011;M2010;\n")

YEARS_REQUIRED = ['2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']
CHARS_TO_KEEP = "T"

# Variables globales para el gráfico de R3
YEARS_POBLATION_GRAPH = ['2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']
CHAR_TO_KEEP_GRAPH = "T"
NUMBER_AUTONOMIES = 10

# Variable directorio

SALIDAHTML = DIRECTORIO_RESULTADOS + "variacionComAutonomas.html"

FILE_TO_READ = DIRECTORIO_ENTRADAS + "poblacionProvinciasHM2010-17.csv"


def r5():
    array_autonomies_name_sorted, dict_autonomies_graph = obtener_etiqueta_array_dict_for_graph(FILE_TO_READ,
                                                                                                FIRST_WORD, LAST_WORD,
                                                                                                CHARS_TO_KEEP,
                                                                                                CHAR_TO_KEEP_GRAPH,
                                                                                                YEARS_REQUIRED,
                                                                                                YEARS_POBLATION_GRAPH,
                                                                                                CABECERA,
                                                                                                NUMBER_AUTONOMIES)

    directorio_archivo = lineal_graph(YEARS_POBLATION_GRAPH, dict_autonomies_graph, array_autonomies_name_sorted)
    include_graph_in_html(SALIDAHTML, "../" + directorio_archivo, "Grafico de lineas de la "
                                                                   "poblacion por comunidad")


# funcion para guardar el grafico de lineas, devuelve la ubicacion del archivo
def lineal_graph(x_ticks, dict_autonomies_graph, array_autonomies_name_sorted):
    plt.figure("lineal")
    plt.title("Población total en 2010-2017 (CCAA)")  # Establece el título del gráfico
    for autonomy in array_autonomies_name_sorted:
        plt.plot(dict_autonomies_graph[autonomy][len(YEARS_POBLATION_GRAPH):0:-1], marker="o", label=autonomy)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.xticks(np.arange(len(YEARS_POBLATION_GRAPH)), YEARS_POBLATION_GRAPH[::-1])
    directorio_archivo = DIRECTORIO_IMAGENES + "R5.png"
    plt.savefig(DIRECTORIO_IMAGENES + 'R5.png', bbox_inches='tight')

    return directorio_archivo


if __name__ == "R5":  # Cada vez que lo importe se ejecutará  lo que esté aquí dentro
    print("Importando y ejecutando R5.py")
    r5()

if __name__ == "__main__":  # Si lo ejecuto como fichero principal, se ejecuta lo que hay aquí dentro
    r5()
