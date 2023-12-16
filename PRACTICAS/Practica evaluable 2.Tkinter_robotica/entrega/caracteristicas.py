import json
import math
import os
import csv
import globals

# en caracteristicas

dat_piernas = "piernasDataset.dat"
dat_no_piernas = "noPiernasDataset.dat"
csv_piernas = globals.piernasDataset


def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def calculate_width(points):
    return euclidean_distance(points[0], points[len(points) - 1])


def calculate_perimeter(points):
    perimeter = 0

    for i in range(len(points) - 1):
        perimeter += euclidean_distance(points[i], points[i + 1])

    return perimeter


# (depth) es el máximo de las distancias de la recta P1Pn a los puntos P1 a Pn
def calculate_depth(points):
    # calculamos la recta P1Pn
    p1 = points[0]
    pn = points[len(points) - 1]

    A = pn[1] - p1[1]
    B = p1[0] - pn[0]
    C = pn[0] * p1[1] - pn[1] * p1[0]

    # calculamos la distancia de cada punto a la recta
    max_distance = 0

    for i in range(1, len(points) - 1):
        denominator = math.sqrt(A ** 2 + B ** 2)
        if denominator != 0:
            distance = abs(A * points[i][0] - B * points[i][1] + C) / denominator
        else:
            distance = 0

        if distance > max_distance:
            max_distance = distance
    return max_distance


def caracteristics_to_dat(saved_json, dat_file, piernas):
    # leemos clustersPiernas.json y por cada cluster cogemos sus puntos y lo almacenamos
    clusters = []
    with open(saved_json, "r") as f:
        for line in f:
            clusters.append(json.loads(line))

    for cluster in clusters:
        puntos = []
        for i in range(len(cluster["puntosX"])):
            x = cluster["puntosX"][i]
            y = cluster["puntosY"][i]
            puntos.append([x, y])

        # calculamos la distancia euclidea entre los puntos
        perimetro = calculate_perimeter(puntos)
        anchura = calculate_width(puntos)
        profundidad = calculate_depth(puntos)

        with open(dat_file, "a") as f:
            caracteristics = {
                "numero_cluster": cluster["numero_cluster"],
                "perimetro": perimetro,
                "anchura": anchura,
                "profundidad": profundidad,
                "esPierna": piernas
            }
            f.write(json.dumps(caracteristics) + '\n')


def eliminar_ficheros():
    if os.path.exists(dat_piernas):
        os.remove(dat_piernas)
    if os.path.exists(dat_no_piernas):
        os.remove(dat_no_piernas)
    if os.path.exists(csv_piernas):
        os.remove(csv_piernas)


def dat_to_csv(all_caracteristicas):
    with open(csv_piernas, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for caracteristica in all_caracteristicas:
            writer.writerow([format(caracteristica['perimetro'], '.2f'),
                             format(caracteristica['anchura'], '.2f'),
                             format(caracteristica['profundidad'], '.2f'),
                             caracteristica['esPierna']]
                            )


def caracteristicas():
    eliminar_ficheros()

    caracteristics_to_dat(globals.piernas_json, dat_piernas, 1)
    caracteristics_to_dat(globals.no_piernas_json, dat_no_piernas, 0)

    # convertimos los ficheros .dat a .csv
    all_caracteristics = []
    with open(dat_piernas, "r") as f:
        for line in f:
            all_caracteristics.append(json.loads(line))

    with open(dat_no_piernas, "r") as f:
        for line in f:
            all_caracteristics.append(json.loads(line))

    dat_to_csv(all_caracteristics)
