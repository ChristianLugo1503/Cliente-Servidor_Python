import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class Ventana1:
    def __init__(self, master):
        self.master = master
        self.master.title("Cliente")
        self.master.geometry("300x200")

        etiqueta_nombre = tk.Label(self.master, text="¡Bienvenido!\nIngrese su nombre:")
        etiqueta_nombre.pack(pady=10)

        self.entrada_nombre = tk.Entry(self.master)
        self.entrada_nombre.pack(pady=10)

        self.boton_siguiente = tk.Button(master, text="Continuar", command=self.ir_a_ventana2)
        self.boton_siguiente.pack(pady=20)

    def ir_a_ventana2(self):
        nombre = self.entrada_nombre.get()
        self.master.withdraw()
        ventana2 = tk.Toplevel(self.master)
        segunda_ventana = Ventana2(ventana2, nombre)

class Ventana2:
    def __init__(self, master, nombre):
        self.master = master
        self.master.title("Cliente")
        self.master.geometry("550x600")

        #Mensaje de bienvenida por medio de un label
        etiqueta_nombre = tk.Label(self.master, text=f"¡Bienvenido! {nombre}!")
        etiqueta_nombre.pack(pady=20)

        #Creacion y configuracion del listbox
        lista = tk.Listbox(self.master, selectmode=tk.SINGLE)
        lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        lista.place(relx=0.10, rely=0.10)
        lista.config(width=70, height=25)
        #Creacion y configuracion del scrollbar
        scrollbar = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=lista.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        lista.config(yscrollcommand=scrollbar.set) #La barra de desplazamiento afecta el listBox

        #entrada del mensaje
        self.entrada_texto = tk.Entry(self.master)
        self.entrada_texto.pack(pady=10)
        self.entrada_texto.place(relx=0.100, rely=0.800)
        self.entrada_texto.config(width=50)

        #Boton para enviar el mensaje
        self.enviar = tk.Button(master, text="Enviar mensaje", command="")
        self.enviar.pack(pady=20)
        self.enviar.place(relx=0.700, rely=0.800)
        
        #Boton para salir
        self.boton_regresar = tk.Button(master, text="Salir", command=lambda: self.ir_a_ventana1())
        self.boton_regresar.pack(pady=20)
        self.boton_regresar.place(relx=0.500, rely=0.900)

    def ir_a_ventana1(self):
        self.master.destroy()
        ventana1 = tk.Tk()
        primera_ventana = Ventana1(ventana1)
        ventana1.mainloop()

ventana_principal = tk.Tk()
app_ventana1 = Ventana1(ventana_principal)
ventana_principal.mainloop()