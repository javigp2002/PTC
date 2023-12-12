from tkinter import *
from accion_botones import *
from globals import *

debug_mode = False


def connect_to_vrep():
    clientId = get_client_id_vrep()

    if clientId != -1:
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


def toggle_debug_mode():
    global debug_mode
    debug_mode = not debug_mode
    if debug_mode:
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


def main():
    global raiz
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

    b_stop_disconnect_vrep = Button(root, text="Detener y desconectar VREP", state=DISABLED)
    b_stop_disconnect_vrep.grid(row=r, column=0)
    r += 1

    l_estado = Label(root, text="Estado: No conectado a VREP")
    l_estado.grid(row=r, column=0)
    r += 1

    b_capturar = Button(root, text="Capturar", state=DISABLED)
    b_capturar.grid(row=r, column=0)
    r += 1

    b_agrupar = Button(root, text="Agrupar", state=DISABLED)
    b_agrupar.grid(row=r, column=0)
    r += 1

    b_extraer = Button(root, text="Extraer características", state=DISABLED)
    b_extraer.grid(row=r, column=0)
    r += 1

    b_entrenar = Button(root, text="Entrenar clasificador", state=DISABLED)
    b_entrenar.grid(row=r, column=0)
    r += 1

    b_predecir = Button(root, text="Predecir", state=DISABLED)
    b_predecir.grid(row=r, column=0)
    r += 1

    b_salir = Button(root, text="Salir", command=lambda: salir(b_stop_disconnect_vrep["state"] == NORMAL))
    b_salir.grid(row=r, column=0)
    r += 1

    b_debug = Button(root, text="Debug", command=toggle_debug_mode)
    b_debug.grid(row=r, column=0)
    r += 1

    # Second Column of params
    r = 0

    # Second Column

    parametros_label = Label(root, text="Parámetros:")
    parametros_label.grid(row=r, column=1)
    r += 1

    iteraciones_label = Label(root, text="Iteraciones:")
    iteraciones_label.grid(row=r, column=1)
    iteraciones = Entry(root)
    iteraciones.insert(0, ITERACION_DEFAULT)
    iteraciones.grid(row=r, column=2)

    r += 1

    cerca_label = Label(root, text="Cerca:")
    cerca_label.grid(row=r, column=1)
    cerca = Entry(root)
    cerca.insert(0, CERCA_DEFAULT)
    cerca.grid(row=r, column=2)
    r += 1

    media_label = Label(root, text="Media:")
    media_label.grid(row=r, column=1)
    media = Entry(root)
    media.insert(0, MEDIA_DEFAULT)
    media.grid(row=r, column=2)
    r += 1

    lejos_label = Label(root, text="Lejos: ")
    lejos_label.grid(row=r, column=1)
    lejos = Entry(root)
    lejos.insert(0, LEJOS_DEFAULT)
    lejos.grid(row=r, column=2)
    r += 1

    min_puntos_label = Label(root, text="MinPuntos:")
    min_puntos_label.grid(row=r, column=1)
    min_puntos = Entry(root)
    min_puntos.insert(0, MIN_PUNTOS_DEFAULT)
    min_puntos.grid(row=r, column=2)
    r += 1

    max_puntos_label = Label(root, text="MaxPuntos:")
    max_puntos_label.grid(row=r, column=1)
    max_puntos = Entry(root)
    max_puntos.insert(0, MAX_PUNTOS_DEFAULT)
    max_puntos.grid(row=r, column=2)
    r += 1

    umbral_distancia_label = Label(root, text="UmbralDistancia:")
    umbral_distancia_label.grid(row=r, column=1)
    umbral_distancia = Entry(root)
    umbral_distancia.insert(0, UMBRAL_DISTANCIA_DEFAULT)
    umbral_distancia.grid(row=r, column=2)
    r += 1

    def upload():
        # TODO: Implement upload functionality
        pass

    upload_button = Button(root, text="Upload", command=upload)
    upload_button.grid(row=r, column=2)

    # Third Column
    lectura = Label(root, text="Fichero para la captura:")
    lectura.grid(row=0, column=3)
    r += 1

    listbox = Listbox(root, width=35, height=12)
    listbox.grid(row=1, column=3, rowspan=8)

    # Third Column

    # Configure column widths
    root.grid_columnconfigure(0, weight=2, uniform="columns")
    root.grid_columnconfigure(1, weight=1, uniform="columns")
    root.grid_columnconfigure(2, weight=1, uniform="columns")
    root.grid_columnconfigure(3, weight=2, uniform="columns")

    raiz = root

    root.mainloop()


if __name__ == "__main__":
    main()
