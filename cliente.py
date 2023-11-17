import socket
import threading
import tkinter as tk
from tkinter import messagebox

class Ventana1:
    def __init__(self, master):
        self.master = master
        self.master.title("Cliente")
        self.master.geometry("300x200")

        etiqueta_nombre = tk.Label(self.master, text="¡Bienvenido!\nIngrese su nombre:")
        etiqueta_nombre.pack(pady=10)

        self.entrada_nombre = tk.Entry(self.master)
        self.entrada_nombre.pack(pady=10)
        self.entrada_nombre.bind("<Return>", lambda event: self.ir_a_ventana2())

        self.boton_siguiente = tk.Button(master, text="Continuar", command=self.ir_a_ventana2)
        self.boton_siguiente.pack(pady=20)

    def ir_a_ventana2(self):
        nombre = self.entrada_nombre.get()
        
        # verificar si el campo nombre esta vacio
        if not nombre.strip():  
            tk.messagebox.showerror("Error", "Por favor, ingrese su nombre.")
            return
        
        self.master.withdraw()
        ventana2 = tk.Toplevel(self.master)
        segunda_ventana = Ventana2(ventana2, nombre)

class Ventana2:
    def __init__(self, master, nombre):
        self.master = master
        self.master.title("Cliente")
        self.master.geometry("550x600")

        etiqueta_nombre = tk.Label(self.master, text=f"¡Bienvenido! {nombre}!")
        etiqueta_nombre.pack(pady=20)

        self.lista = tk.Listbox(self.master, selectmode=tk.SINGLE)
        self.lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.lista.place(relx=0.10, rely=0.10)
        self.lista.config(width=70, height=25)

        scrollbar = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.lista.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista.config(yscrollcommand=scrollbar.set)

        self.entrada_texto = tk.Entry(self.master)
        self.entrada_texto.pack(pady=10)
        self.entrada_texto.place(relx=0.100, rely=0.800)
        self.entrada_texto.config(width=50)
        self.entrada_texto.bind("<Return>", lambda event: self.btnEnviar(nombre, self.entrada_texto.get()))

        self.enviar = tk.Button(master, text="Enviar mensaje", command=lambda: self.btnEnviar(nombre, self.entrada_texto.get()))
        self.enviar.pack(pady=20)
        self.enviar.place(relx=0.700, rely=0.800)

        self.boton_regresar = tk.Button(master, text="Salir", command=lambda: self.ir_a_ventana1(nombre))
        self.boton_regresar.pack(pady=20)
        self.boton_regresar.place(relx=0.500, rely=0.900)

        host = '127.0.0.1'
        port = 55555

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

        receive_thread = threading.Thread(target=self.receive_messages, args=(self.client, nombre))
        receive_thread.start()

    def receive_messages(self, cliente, username):
        try:
            while True:
                message = cliente.recv(1024).decode('utf-8')
                if message == "@username":
                    cliente.send(username.encode("utf-8"))
                else:
                    self.lista.insert(tk.END, message)
        except Exception as e:
            self.lista.insert(tk.END, f"\nHa ocurrido un error: {e}")
            cliente.close()

    def write_messages(self, username, message):
        mensaje = f"{username}: {message}"
        self.client.send(mensaje.encode('utf-8'))
        self.lista.insert(tk.END, f"        {message}")

    def btnEnviar(self, username, message):
        write_thread = threading.Thread(target=self.write_messages, args=(username, message))
        write_thread.start()
        # limpiar el texto del input
        self.entrada_texto.delete(0, tk.END)

    def ir_a_ventana1(self, username):
        mensaje = f"{username} salió del chat"
        self.client.send(mensaje.encode('utf-8'))
        self.client.close()
        
        self.master.destroy()
        ventana1 = tk.Tk()
        primera_ventana = Ventana1(ventana1)
        ventana1.mainloop()

ventana_principal = tk.Tk()
app_ventana1 = Ventana1(ventana_principal)
ventana_principal.mainloop()
