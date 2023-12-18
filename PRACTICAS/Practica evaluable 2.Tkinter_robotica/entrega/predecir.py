"""Ahora hay que crear un script llamado “predecir.py” que:  Reciba los datos de laser  Los convierta en clústeres
 Genere las tres características de cada clúster  Utilice el predictor para cada clúster a partir de sus
características  Dibuje en color rojo aquellos clústeres que sean piernas según el predictor y en azul aquellos que
no. Cuando se detecte dos clústeres “cercanos” que pertenezcan a un mismo objeto o persona, se debe calcular el
centroide de ambos clústeres y pintar un punto rojo (o azul) en el punto medio del segmento que une ambos centroides,
entendiendo que ese punto representa la posición de la persona/objeto detectada/o. Este gráfico se almacena en
fichero .jpg y se salva en la carpeta “predicción”."""

import json
import os
import sys
import glob
import math
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import globals
import sim as vrep
import caracteristicas
import pickle
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
import agrupar
import caracteristicas

def distance_between_clusters(points1, points2):
    for point in points1:
        for point2 in points2:
            distance = math.sqrt((point[0] - point2[0]) ** 2 + (point[1] - point2[1]) ** 2)
            if distance < 0.2:
                return True

def calculate_centroide(points):
    x = 0
    y = 0
    for point in points:
        x += point[0]
        y += point[1]
    return [x / len(points), y / len(points)]


def recibir_datos_laser():
    clientID = globals.clientId

    _, robothandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)

    # Guardar la referencia de los motores
    _, left_motor_handle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
    _, right_motor_handle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)

    # Guardar la referencia de la camara
    _, camhandle = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)

    # acceder a los datos del laser
    _, datosLaserComp = vrep.simxGetStringSignal(clientID, 'LaserData', vrep.simx_opmode_streaming)

    velocidad = 0  # Variable para la velocidad de los motores, dejamos fijo el robot

    time.sleep(1)

    # Iniciar la camara y esperar un segundo para llenar el buffer
    _, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)
    returnCode, signalValue = vrep.simxGetStringSignal(clientID, 'LaserData', vrep.simx_opmode_buffer)

    datosLaser = vrep.simxUnpackFloats(signalValue)

    return datosLaser


def convert_data_to_cluster(data):



    # convertimos los datos a cluster
    puntosx = []  # listas para recibir las coordenadas x, y z de los puntos detectados por el laser
    puntosy = []

    for indice in range(0, len(data), 3):
        puntosx.append(data[indice + 1])
        puntosy.append(data[indice + 2])

    # agrupamos los puntos en clusters
    clusters = agrupar.group_in_clusters(puntosx, puntosy)

    if os.path.exists("clusters_prediccion.json"):
        os.remove("clusters_prediccion.json")
        print("Borrando el fichero: ", "clusters_prediccion.json")

    agrupar.save_clusters(clusters, "clusters_prediccion.json")

    return clusters


def predecir():
    directorio_inicial = os.getcwd()
    if not os.path.exists("prediccion"):
        os.mkdir("prediccion")
    os.chdir("prediccion")

    datosLaser = recibir_datos_laser()

    clusters = convert_data_to_cluster(datosLaser)

    caracteristicas_a_predecir = np.zeros((len(clusters), 3))

    i = 0
    for cluster in clusters:
        puntos = cluster

        # calculamos la distancia euclidea entre los puntos
        perimetro = caracteristicas.calculate_perimeter(puntos)
        anchura = caracteristicas.calculate_width(puntos)
        profundidad = caracteristicas.calculate_depth(puntos)

        caracteristicas_a_predecir[i] = [perimetro, anchura, profundidad]
        i += 1

    print("directorio: ", os.getcwd())
    clasificador = "../" + globals.clasificador_pkl

    with open(clasificador, 'rb') as f:
        clf = pickle.load(f)

    # predecimos

    y_pred = clf.predict(caracteristicas_a_predecir)

    df = pd.DataFrame(caracteristicas_a_predecir, columns=['perimetro', 'anchura', 'profundidad'])
    df['esPierna'] = y_pred

    plt.clf()
    plt.axis('tight')
    plt.axis([1, 3.6, -2.4, 2.4])

    for i in range(len(df)):
        puntos = clusters[i]

        if y_pred[i] == 1:
            color = 'r.'
        else:
            color = 'b.'

        for j in range(len(puntos)):
            plt.plot(puntos[j][0], puntos[j][1], color)

        ## comparamos con los siguientes cluster si la distancia entre ellos es menor que 0.5
        for j in range(i + 1, len(df)):
            puntos2 = clusters[j]
            if distance_between_clusters(puntos, puntos2):
                # calcular centroide de los dos clusters
                centroide_a = calculate_centroide(puntos)
                centroide_b = calculate_centroide(puntos2)

                # punto medio de los segmentos
                x = (centroide_a[0] + centroide_b[0]) / 2
                y = (centroide_a[1] + centroide_b[1]) / 2

                plt.plot(x, y, 'g. ')

    plt.savefig('prediccion.jpg')
    os.chdir(directorio_inicial)
