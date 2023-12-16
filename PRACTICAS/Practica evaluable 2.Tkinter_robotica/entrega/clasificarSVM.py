"""
Entrenar clasificador binario utilizando SVM y scikit-learn.

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import GridSearchCV
import pickle
import globals

# import warnings filter
from warnings import simplefilter

###


def entrenar_segun_clasificador(X, y, svclassifier, svc_cross_validation):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=25)
    svclassifier.fit(X_train, y_train)

    # Realizamos la predicción
    y_pred = svclassifier.predict(X_test)
    acc_test = accuracy_score(y_test, y_pred)

    print("Accuracy en test: ", acc_test)
    print("Matriz de confusión: \n", confusion_matrix(y_test, y_pred))

    # Cross validation
    print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
    print("f1-score es la media entre precisión y recall")
    print(classification_report(y_test, y_pred))

    # Cross validation
    print("Cross validation")
    scores = cross_val_score(svc_cross_validation, X, y, cv=5)
    print("Accuracy 5-cross validation: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))

    # Realizamos la predicción


def entrenar_clasificador():
    grado_kernel_pol = 3

    # ignore all future warnings
    simplefilter(action='ignore', category=FutureWarning)
    simplefilter(action='ignore', category=DeprecationWarning)

    # Cargamos el dataset
    colnames = ["perimetro", "anchura", "profundidad", "esPierna"]

    dataset = pd.read_csv(globals.piernasDataset, names=colnames)


    # Separamos las características de las etiquetas
    X = dataset.drop('esPierna', axis=1)
    y = dataset['esPierna']

    entrenar_segun_clasificador(X, y, SVC(kernel='linear'), SVC(kernel='linear'))
    entrenar_segun_clasificador(X, y, SVC(kernel='poly', degree=grado_kernel_pol), SVC(kernel='poly', degree=grado_kernel_pol))
    entrenar_segun_clasificador(X, y, SVC(kernel='rbf'), SVC(kernel='rbf'))

    #######################
    # Kernel radial
    #######################


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=25)


    print("Búsqueda de parámetros en un rango en el caso de RBF")

    param_grid={'C':[1,10,100,1000],
                'gamma': [0.001, 0.005, 0.01, 0.1]}

    clf=GridSearchCV(SVC(kernel='rbf'), param_grid)

    clf=clf.fit(X_train, y_train)
    print("Mejor estimador encontrado")

    print(clf.best_estimator_)

    mejorSVC=clf.best_estimator_

    y_pred = mejorSVC.predict(X_test)
    acc_test = accuracy_score(y_test, y_pred)

    print("Accuracy en test: ", acc_test)

    print("Matriz de confusión: \n", confusion_matrix(y_test, y_pred))

    print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
    print("f1-score es la media entre precisión y recall")
    print(classification_report(y_test, y_pred))

    # Cross validation
    print("Cross validation")
    svcRadial2 = SVC(kernel='rbf')
    scores = cross_val_score(svcRadial2, X, y, cv=5)

    print("Accuracy 5-cross validation: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))

    # Guardamos el modelo
    with open(globals.clasificador_pkl, "wb") as archivo:
        pickle.dump(mejorSVC, archivo)


