from tkinter import messagebox
import sim
import sys
import globals


def salir(desconectado):
    if desconectado:
        messagebox.showerror("Error", "Debe desconectarse de VREP antes de salir.")
    else:
        respuesta = messagebox.askyesno("Salir", "¿Desea salir de la aplicación?")
        if respuesta:
            sys.exit(0)


def get_client_id_vrep():
    print("Conectando a VREP")
    # Conectamos al servidor de VREP
    sim.simxFinish(-1)  # Terminar todas las conexiones
    globals.clientId = sim.simxStart('127.0.0.1', 19999, True, True, 5000,
                                     5)  # Iniciar una nueva conexion en el puerto 19999 (direccion por defecto)

    return globals.clientId
