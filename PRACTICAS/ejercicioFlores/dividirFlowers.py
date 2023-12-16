"""
Hay 17 tipos de flowers en dataset/classes.txt y vamos a dividirlos en distintos directorios
Hay que implementar un programa en Python que sea capaz de crear una carpeta por cada
clase y copiar sus correspondientes imágenes a la vez que se renombran a
"image_9999_clase_n.jpg". Es decir dentro de “daffodil” se deberían llamar
image_0001_daffodil_1.jpg a image_0080_daffodil_80.jpg y así con cada clase.
"""

import os
import glob
import shutil


# leemos el fichero classes.txt y guardamos las clases en una lista
def leer_clases():
    clases = []
    with open("dataset/classes.txt", "r") as f:
        for linea in f:
            clases.append(linea.strip())

    return clases


# creamos los directorios para cada clase
def crear_directorios(clases):
    for clase in clases:
        if not os.path.exists(clase):
            os.makedirs(clase)


#
def copiar_imagenes():
    clases = leer_clases()
    crear_directorios(clases)

    lista_imagenes = sorted(glob.glob("dataset/*.jpg"))

    num_imagen = 1
    for clase in clases:
        for i in range(80):
            new_name = clase + "/image_" + str(num_imagen).zfill(4) + "_" + clase + "_" + str(i+1) + ".jpg"
            shutil.copy(lista_imagenes[num_imagen-1], new_name)

            num_imagen += 1


copiar_imagenes()
