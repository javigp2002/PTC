import os.path
from tkinter import *
from accion_botones import *
import globals
import capturar
from agrupar import agrupar
from caracteristicas import caracteristicas
from clasificarSVM import entrenar_clasificador
from predecir import predecir

global raiz



def main():

    def connect_to_vrep():
        get_client_id_vrep()

        if globals.clientId != -1:
            l_estado.config(text="Estado: Conectado a VREP")
            b_stop_disconnect_vrep.config(state=NORMAL)
            b_capturar.config(state=NORMAL)
            messagebox.showinfo("Conexión", "Conexión con VREP establecida")
        else:
            messagebox.showerror("Conexión", "Debe iniciar el simulador.")

    def disconnect_to_vrep():
        l_estado.config(text="Estado: No conectado a VREP")
        b_stop_disconnect_vrep.config(state=DISABLED)
        b_capturar.config(state=DISABLED)
        messagebox.showinfo("Desconexión", "Desconexión con VREP establecida")

    def upload():
        global raiz

        globals.iteraciones_str = str(iteraciones.get())
        globals.cerca_str = str(cerca.get())
        globals.media_str = str(media.get())
        globals.lejos_str = str(lejos.get())
        globals.min_puntos_str = str(min_puntos.get())
        globals.max_puntos_str = str(max_puntos.get())
        globals.umbral_distancia_str = str(umbral_distancia.get())
        show_params()

    def show_params():
        ventana = Toplevel(root)

        # Crear y empaquetar etiquetas para cada parámetro
        Label(ventana, text="Nuevos valores de los parámetros:").pack()
        Label(ventana, text="Iteraciones: " + str(globals.iteraciones_str)).pack()
        Label(ventana, text="Cerca: " + str(globals.cerca_str)).pack()
        Label(ventana, text="Media: " + str(globals.media_str)).pack()
        Label(ventana, text="Lejos: " + str(globals.lejos_str)).pack()
        Label(ventana, text="MinPuntos: " + str(globals.min_puntos_str)).pack()
        Label(ventana, text="MaxPuntos: " + str(globals.max_puntos_str)).pack()
        Label(ventana, text="UmbralDistancia: " + str(globals.umbral_distancia_str)).pack()

    def capture():
        file = ficheros.get(ANCHOR)
        if not file:
            messagebox.showwarning(message="Debe elegir un fichero de la lista")
        else:
            # si se ha elegido un fichero comprobamos que existe o creamos uno nuevo
            directory = os.path.dirname(file)

            if not os.path.isdir(directory):
                os.makedirs(directory)

            if os.path.exists(file):
                answer = messagebox.askyesno(message="El fichero ya existe, ¿desea sobreescribirlo?")
                if answer:
                    os.remove(file)
                else:
                    return
            else:
                answer = messagebox.askyesno(message="El fichero no existe, ¿desea crearlo?")

            if answer:
                with open(file, "w") as f:
                    f.close()

            capturar.main(file)

            b_agrupar.config(state=NORMAL)

    def group():
        agrupar()
        ##
        b_extraer.config(state=NORMAL)

    def extract_caracteristics():
        caracteristicas()
        messagebox.showinfo("Extracción de características", "Extracción de características finalizada")

    def entrenar_clasif():
        entrenar_clasificador()
        messagebox.showinfo("Entrenamiento", "Entrenamiento finalizado")

    def predict():
        predecir()
        messagebox.showinfo("Predicción", "Predicción finalizada")

    def toggle_debug_mode():
        globals.debug_mode = not globals.debug_mode
        if globals.debug_mode:
            # Habilitar los botones b_
            b_stop_disconnect_vrep.config(state=NORMAL)
            b_capturar.config(state=NORMAL)
            b_agrupar.config(state=NORMAL)
            b_extraer.config(state=NORMAL)
            b_entrenar.config(state=NORMAL)
            b_predecir.config(state=NORMAL)
        else:
            # Deshabilitar los botones b_
            b_stop_disconnect_vrep.config(state=DISABLED)
            b_capturar.config(state=DISABLED)
            b_agrupar.config(state=DISABLED)
            b_extraer.config(state=DISABLED)
            b_entrenar.config(state=DISABLED)
            b_predecir.config(state=DISABLED)

    root = Tk()

    root.geometry("700x300")
    # First Column
    r = 0
    label1 = Label(root, text="Es necesario ejectuar el simulador VREP")
    label1.grid(row=0, column=0)

    r += 1
    b_connect_vrep = Button(root, text="Conectar con VREP", command=connect_to_vrep)
    b_connect_vrep.grid(row=r, column=0)

    r += 1
    b_stop_disconnect_vrep = Button(root, text="Detener y desconectar VREP", state=DISABLED, command=disconnect_to_vrep)
    b_stop_disconnect_vrep.grid(row=r, column=0)

    r += 1
    l_estado = Label(root, text="Estado: No conectado a VREP")
    l_estado.grid(row=r, column=0)

    r += 1
    b_capturar = Button(root, text="Capturar", state=DISABLED, command=capture)
    b_capturar.grid(row=r, column=0)

    r += 1
    b_agrupar = Button(root, text="Agrupar", state=DISABLED, command=group)
    b_agrupar.grid(row=r, column=0)

    r += 1
    b_extraer = Button(root, text="Extraer características", state=DISABLED, command=extract_caracteristics)
    b_extraer.grid(row=r, column=0)

    r += 1
    b_entrenar = Button(root, text="Entrenar clasificador", state=DISABLED, command=entrenar_clasif)
    b_entrenar.grid(row=r, column=0)

    r += 1
    b_predecir = Button(root, text="Predecir", state=DISABLED, command=predict)
    b_predecir.grid(row=r, column=0)

    r += 1
    b_salir = Button(root, text="Salir", command=lambda: salir(b_stop_disconnect_vrep["state"] == NORMAL))
    b_salir.grid(row=r, column=0)

    r += 1
    b_debug = Button(root, text="Debug", command=toggle_debug_mode)
    b_debug.grid(row=r, column=0)

    r += 1
    # Second Column of params

    # Second Column
    r = 0
    parametros_label = Label(root, text="Parámetros:")
    parametros_label.grid(row=r, column=1)

    r += 1
    iteraciones_label = Label(root, text="Iteraciones:")
    iteraciones_label.grid(row=r, column=1)
    iteraciones = Entry(root)
    iteraciones.insert(0, globals.iteraciones_str)

    iteraciones.grid(row=r, column=2)

    r += 1
    cerca_label = Label(root, text="Cerca:")
    cerca_label.grid(row=r, column=1)
    cerca = Entry(root)
    cerca.insert(0, globals.cerca_str)
    cerca.grid(row=r, column=2)

    r += 1
    media_label = Label(root, text="Media:")
    media_label.grid(row=r, column=1)
    media = Entry(root)
    media.insert(0, globals.media_str)
    media.grid(row=r, column=2)

    r += 1
    lejos_label = Label(root, text="Lejos: ")
    lejos_label.grid(row=r, column=1)
    lejos = Entry(root)
    lejos.insert(0, globals.lejos_str)
    lejos.grid(row=r, column=2)

    r += 1
    min_puntos_label = Label(root, text="MinPuntos:")
    min_puntos_label.grid(row=r, column=1)
    min_puntos = Entry(root)
    min_puntos.insert(0, globals.min_puntos_str)
    min_puntos.grid(row=r, column=2)

    r += 1
    max_puntos_label = Label(root, text="MaxPuntos:")
    max_puntos_label.grid(row=r, column=1)
    max_puntos = Entry(root)
    max_puntos.insert(0, globals.max_puntos_str)
    max_puntos.grid(row=r, column=2)

    r += 1
    umbral_distancia_label = Label(root, text="UmbralDistancia:")
    umbral_distancia_label.grid(row=r, column=1)
    umbral_distancia = Entry(root)
    umbral_distancia.insert(0, globals.umbral_distancia_str)
    umbral_distancia.grid(row=r, column=2)

    r += 1

    upload_button = Button(root, text="Upload", command=upload)
    upload_button.grid(row=r, column=2)

    # Third Column
    lectura = Label(root, text="Fichero para la captura:")
    lectura.grid(row=0, column=3)
    r += 1

    ficheros = Listbox(root, width=35, height=12)
    ficheros.grid(row=1, column=3, rowspan=8)

    # LISTBOX PARA LA COLUMNA 3
    file_names = [
        "positivo1/enPieCerca.json", "positivo2/enPieMedia.json", "positivo3/enPieLejos.json",
        "positivo4/sentadoCerca.json", "positivo5/sentadoMedia.json", "positivo6/sentadoLejos.json",
        "negativo1/cilindroMenorCerca.json", "negativo2/cilindroMenorMedia.json", "negativo3/cilindroMenorLejos.json",
        "negativo4/cilindroMayorCerca.json", "negativo5/cilindroMayorMedia.json", "negativo6/cilindroMayorLejos.json"
    ]

    for file_name in file_names:
        ficheros.insert(END, file_name)

    # Configure column widths
    root.grid_columnconfigure(0, weight=2, uniform="columns")
    root.grid_columnconfigure(1, weight=1, uniform="columns")
    root.grid_columnconfigure(2, weight=1, uniform="columns")
    root.grid_columnconfigure(3, weight=2, uniform="columns")

    raiz = root

    root.mainloop()


if __name__ == "__main__":
    main()
