"""
Vamos a definir un clúster como un conjunto de puntos cercanos y que pueden ser candidatos a formar una única pierna. Primero hay que establecer el número mínimo y máximo de puntos que puede tener un clúster. Hay que definirlos como parámetros llamados “MinPuntos” y “MaxPuntos” y según los datos de la experimentación, establecer los más apropiados.

Tened en cuenta que cuando las personas están más lejos, losclústeres pueden estar formados por menos puntos. Para agrupar los puntos de los ficheros anteriores en clústeres hay que utilizar el algoritmo de “agrupación por distancia de salto”. Se crea un clúster como una lista de puntos, se mete el primer punto, ahora se analiza el segundo punto para ver si se incorpora al clúster actual. Si la distancia del punto anterior al que se está analizando es menor a un umbral (parámetro “umbralDistancia”), entonces se incorpora el punto analizado al clúster y se pasa al siguiente. El cluster actual puede finalizar por dos motivos: que el punto analizado está más lejos del umbral de distancia o bien que se ha superado el punto máximo de puntos (MaxPuntos) que puede tener un cluster. Para aceptar un grupo de puntos como clúster válido tened en cuenta que debe tener un número mínimo de puntos (MinPuntos) además de cumplir con el valor máximo (MaxPuntos).
A partir de las carpetas de ejemplos positivos y negativos se deben generar solo dos ficheros, uno que llamaremos clustersPiernas.json y otro clustersNoPiernas.json con el siguiente formato de cada línea usando diccionarios y el módulo json:
{“numero_cluster”:i, “numero_puntos”:j, “puntosX”:[lista],”puntosY”:[lista]}

"""

import json
import os
import sys
import glob
import math
import matplotlib.pyplot as plt
import numpy as np
import globals


#
def are_points_distanced(point1, point2):
    distancia_puntos = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    return distancia_puntos <= float(globals.umbral_distancia_str)


def agrupar_by_directories(num_dir_lecturas, lista, saved_json):
    directorio_inicial = os.getcwd()
    # si existe saved_json lo borramos
    if os.path.exists(saved_json):
        os.remove(saved_json)
        print("Borrando el fichero: ", saved_json)

    num_cluster = 0;
    for i in range(num_dir_lecturas):
        os.chdir(lista[i])
        #print("Cambiando el directorio de trabajo a: ", os.getcwd())
        file = glob.glob("*.json")
        objetos = []

        # abrimos el fichero de laser

        with open(file[0], "r") as f:
            for line in f:
                objetos.append(json.loads(line))
        # cerramos el fichero
        f.close()

        # obtenemos los valores de la cabecera
        cabecera = objetos[0]
        segundos = cabecera["TiempoSleep"]
        maxIter = cabecera["MaxIteraciones"]

        # inicializamos las variables
        iteracion = 1
        iteracion_total_dict = objetos[len(objetos) - 1]
        iteracion_total = iteracion_total_dict["Iteraciones totales"]

        plt.axis('equal')
        plt.axis([0, 4, -2, 2])

        clusters = []
        cluster = []

        # volvemos para que los clusters se guarden en el directorio inicial
        os.chdir(directorio_inicial)

        # recorremos las lineas del fichero
        for i in range(iteracion_total):

            iteracion = objetos[i + 1]['Iteracion']
            puntos_x = objetos[i + 1]["PuntosX"]
            puntos_y = objetos[i + 1]["PuntosY"]

            # print("Iteración: ", iteracion, " de ", iteracion_total)

            # plt.clf()
            # plt.plot(puntos_x, puntos_y, 'r.')
            # plt.show()

            # recorremos los puntos de la iteracion
            for j in range(len(puntos_x)):
                # si es el primer punto lo añadimos al cluster
                if j == 0:
                    cluster.append([puntos_x[j], puntos_y[j]])
                else:
                    # si el punto está a una distancia menor al umbral lo añadimos al cluster
                    if are_points_distanced(cluster[-1], [puntos_x[j], puntos_y[j]]):
                        cluster.append([puntos_x[j], puntos_y[j]])
                    else:
                        # Si ha terminado el grupo de puntos entonces comprobar que es válido el cluster
                        if int(globals.min_puntos_str) <= len(cluster) <= int(globals.max_puntos_str):
                            clusters.append(cluster)

                        # reiniciar grupo de puntos
                        cluster = [[puntos_x[j], puntos_y[j]]]

            # añadimos el ultimo cluster
            if int(globals.min_puntos_str) <= len(cluster) <= int(globals.max_puntos_str):
                clusters.append(cluster)

            for cluster_index in range(len(clusters)):

                cluster_dict = {
                    "numero_cluster": num_cluster,
                    "numero_puntos": len(clusters[cluster_index]),
                    globals.puntosX: [punto[0] for punto in clusters[cluster_index]],
                    globals.puntosY: [punto[1] for punto in clusters[cluster_index]]
                }

                num_cluster += 1

                # guardamos el cluster en el fichero
                with open(saved_json, "a") as f:
                    f.write(json.dumps(cluster_dict) + '\n')
            print("clusters añadidos: ", len(clusters), " en la iteracion: ", iteracion)
            clusters = []
            cluster = []

    print ("fin de agrupar_by_directories")




def agrupar():
    print("Directorio de trabajo es: ", os.getcwd())
    lista_positivos = sorted(glob.glob("positivo*"))
    lista_negativos = sorted(glob.glob("negativo*"))

    num_dir_lecturas_positivos = len(lista_positivos)
    num_dir_lecturas_negativos = len(lista_negativos)

    if num_dir_lecturas_positivos > 0 or num_dir_lecturas_negativos > 0:
        print("Numero de directorios con lecturas positivas: ", num_dir_lecturas_positivos, " y negativas: ",
              num_dir_lecturas_negativos)
    else:
        sys.exit("Error, no hay directorios con lecturas positivas")

    agrupar_by_directories(num_dir_lecturas_positivos, lista_positivos, globals.piernas_json)
    agrupar_by_directories(num_dir_lecturas_negativos, lista_negativos, globals.no_piernas_json)
