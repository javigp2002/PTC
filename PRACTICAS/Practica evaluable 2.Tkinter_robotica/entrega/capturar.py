"""
Este script recibe el nombre del fichero (que incluye el directorio)
donde se deben almacenar los valores de la captura. Luego cambia el
directorio de trabajo al directorio creado y usa el nombre de fichero
proporcionado para crear el fichero JSON correspondiente.
"""

import json
import math
import os
import random
import sys
import glob
import time

import cv2
import numpy as np
from matplotlib import pyplot as plt

import globals
import sim as vrep

time_sleep = 0.5

persona_de_pie = "Bill#0"
persona_sentada = "Bill"
cilindro_pequeño = "Cylinder"
cilindro_grande = "Cylinder6"


def main(file):
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

    # Iniciar la camara y esperar un segundo para llenar el buffer
    _, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)
    time.sleep(0.5)

    plt.axis('equal')
    plt.axis([0, 4, -2, 2])

    # mostramos el directorio de trabajo y vemos si existe el dir para salvar los datos
    print("Directorio de trabajo es: ", os.getcwd())
    directorio_inicial = os.getcwd()

    directorio = file.split("/")[0]
    nombreFichero = file.split("/")[1]
    f = open(file, "w")
    f.close()

    if not os.path.isdir(directorio):
        os.mkdir(directorio)

    os.chdir(directorio)
    print("Cambiando el directorio de trabajo: ", os.getcwd())

    # Creamos el fichero JSON para guardar los datos del laser
    # usamos diccionarios
    segundos = time_sleep
    maxIter = int(globals.iteraciones_str)
    iteracion = 1

    cabecera = {"TiempoSleep": segundos,
                "MaxIteraciones": maxIter}

    ficheroLaser = open(nombreFichero, "w")

    _, personhandle = vrep.simxGetObjectHandle(clientID, persona_sentada, vrep.simx_opmode_oneshot_wait)
    # si no es sentado entonces será de pie
    if "positivo" in directorio:
        if "enPie" in nombreFichero:
            _, personhandle = vrep.simxGetObjectHandle(clientID, persona_de_pie, vrep.simx_opmode_oneshot_wait)
    else:
        if "Menor" in nombreFichero:
            _, personhandle = vrep.simxGetObjectHandle(clientID, cilindro_pequeño, vrep.simx_opmode_oneshot_wait)
        else:
            _, personhandle = vrep.simxGetObjectHandle(clientID, cilindro_grande, vrep.simx_opmode_oneshot_wait)

    print("Persona: ", personhandle)

    nombreFicheroSinExtension = nombreFichero.split(".")[0]
    # Según como lo hemos escrito hay que diferenciar la distancia que quermeos seleccionar

    # coger las ultimas 5 letras del nombre del fichero
    if nombreFicheroSinExtension[-5:] == "Cerca":
        distance_min = float(globals.cerca_str)
        distance_max = float(globals.media_str)
    elif nombreFicheroSinExtension[-5:] == "Media":
        distance_min = float(globals.media_str)
        distance_max = float(globals.lejos_str)
    elif nombreFicheroSinExtension[-5:] == "Lejos":
        distance_min = float(globals.lejos_str)
        distance_max = float(globals.lejos_str) + 1
    else:
        sys.exit("Error: el nombre del fichero no es correcto")

    ficheroLaser.write(json.dumps(cabecera) + '\n')

    iters_por_y = 10
    iter_por_x = (round(int(maxIter) / iters_por_y))
    dist_x_por_iter = (distance_max - distance_min) / iter_por_x
    posX = distance_min

    seguir = True

    while iteracion <= maxIter and seguir:

        # Situamos donde queremos a la persona
        # pos será el valor entre la distance maxima y la distancia minima según la iteración
        # posX = random.uniform(distance_min, distance_max)
        posX = distance_min + dist_x_por_iter * ((iteracion - 1) // iters_por_y)

        # calcula la posición en y para que no se salga del radio de 90
        cateto_opuesto = (math.tan(math.pi / 4) * posX)



        # la posicion de y será uniforme desde -cateto_opuesto hasta cateto_opuesto según la iteración
        distance_por_y = cateto_opuesto * 2 / iters_por_y
        posY = -cateto_opuesto + distance_por_y * ((iteracion - 1) % iters_por_y)


        returnCode = vrep.simxSetObjectPosition(clientID, personhandle, -1, [posX, posY, 0.0],
                                                vrep.simx_opmode_oneshot)

        rotation = [0.0, 0.0, (math.pi)/4 * iteracion]
        if "cilindroMayorCerca" in nombreFichero:
            rotation = [0.0, 0.0, 0.0]

        # Cambiamos la orientacion, ojo está en radianes: Para pasar de grados a radianes hay que multiplicar por PI y dividir por 180
        returnCode = vrep.simxSetObjectOrientation(clientID, personhandle, -1, rotation,
                                                   vrep.simx_opmode_oneshot)

        time.sleep(segundos)  # esperamos un tiempo para que el ciclo de lectura de datos no sea muy rápido

        puntosx = []  # listas para recibir las coordenadas x, y z de los puntos detectados por el laser
        puntosy = []
        puntosz = []
        returnCode, signalValue = vrep.simxGetStringSignal(clientID, 'LaserData', vrep.simx_opmode_buffer)

        datosLaser = vrep.simxUnpackFloats(signalValue)
        for indice in range(0, len(datosLaser), 3):
            puntosx.append(datosLaser[indice + 1])
            puntosy.append(datosLaser[indice + 2])
            puntosz.append(datosLaser[indice])

        print("Iteración: ", iteracion)

        # Guardamos los puntosx, puntosy en el fichero JSON
        #        lectura = {"Iteracion": iteracion, "PuntosX: puntosx, "PuntosY": puntosy}
        lectura = {"Iteracion": iteracion, "PuntosX": puntosx, "PuntosY": puntosy}

        # lectura = {"Iteracion": iteracion, globals.puntosX: puntosx, globals.puntosY: puntosy}
        # ficheroLaser.write('{}\n'.format(json.dumps(lectura)))
        ficheroLaser.write(json.dumps(lectura) + '\n')

        # Guardar frame de la camara, rotarlo y convertirlo a BGR
        _, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_buffer)
        img = np.array(image, dtype=np.uint8)
        img.resize([resolution[0], resolution[1], 3])
        img = np.rot90(img, 2)
        img = np.fliplr(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # salvo a disco la imagen

        if iteracion == 1 or iteracion == maxIter:
            cv2.imwrite('Iteracion' + str(iteracion - 1) + '.jpg', img)
            plt.clf()
            plt.plot(puntosx, puntosy, 'r.')
            plt.savefig('Plot' + str(iteracion - 1) + '.jpg')
            plt.show()

        # Mostrar frame y salir con "ESC"
        # cv2.imshow('Image', img)

        tecla = cv2.waitKey(5) & 0xFF
        if tecla == 27:
            seguir = False

        iteracion = iteracion + 1

    # detenemos la simulacion
    vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot_wait)

    # cerramos la conexion
    vrep.simxFinish(clientID)

    # cerramos las ventanas
    cv2.destroyAllWindows()

    finFichero = {"Iteraciones totales": iteracion - 1}
    ficheroLaser.write(json.dumps(finFichero) + '\n')
    ficheroLaser.close()

    ## salimos
    os.chdir(directorio_inicial)
    print("Cambiando el directorio de trabajo: ", os.getcwd())
