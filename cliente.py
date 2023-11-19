import socket
import threading
import tkinter as tk
from tkinter import messagebox

class Ventana1:
    def __init__(self, master):
        self.master = master    #se crea la ventana
        self.master.title("Cliente")    #le asignamos nombre a la ventana
        self.master.geometry("300x200") #se le asigna el tamaño

        etiqueta_nombre = tk.Label(self.master, text="¡Bienvenido!\nIngrese su nombre:") #label de bienvenida
        etiqueta_nombre.pack(pady=10) #espacio entre el label arriba y abajo

        self.entrada_nombre = tk.Entry(self.master) 
        self.entrada_nombre.pack(pady=10)   #espacio entre el input arriba y abajo
        self.entrada_nombre.bind("<Return>", lambda event: self.ir_a_ventana2()) #se asigna para que se pueda enviar con el enter

        self.boton_siguiente = tk.Button(master, text="Continuar", command=self.ir_a_ventana2) #se crea el boton de continuar
        self.boton_siguiente.pack(pady=20)

    def ir_a_ventana2(self): 
        nombre = self.entrada_nombre.get() 
        
        # verificar si el campo nombre esta vacio
        if not nombre.strip():  
            tk.messagebox.showerror("Error", "Por favor, ingrese su nombre.") #en caso de que este vacio envia una ventana emergente
            return
        
        self.master.withdraw()
        ventana2 = tk.Toplevel(self.master)
        segunda_ventana = Ventana2(ventana2, nombre) #se envia el dato nombre a la ventana 2

class Ventana2:
    def __init__(self, master, nombre):
        self.master = master    #se crea la ventana
        self.master.title("Cliente")    #se le asigna nombre
        self.master.geometry("550x600")     #se le asigna tamaño

        etiqueta_nombre = tk.Label(self.master, text=f"¡Bienvenido! {nombre}")  #label con bienvenida
        etiqueta_nombre.pack(pady=20)

        self.lista = tk.Listbox(self.master, selectmode=tk.SINGLE) #se crea un listbox donde se mostraran los mensajes
        self.lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.lista.place(relx=0.10, rely=0.10)  #Se coloca en las coordenadas asignadas
        self.lista.config(width=70, height=25)  #se le asigna el tamaño

        scrollbar = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.lista.yview) #se crea una scrollbar vertical
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista.config(yscrollcommand=scrollbar.set) #Se asigna que el scrollbar afecte a listbox

        self.entrada_texto = tk.Entry(self.master) #se crea un entrada para el mensaje a enviar 
        self.entrada_texto.pack(pady=10)    #se le asigna el espacio de arriba y abajo
        self.entrada_texto.place(relx=0.100, rely=0.800)    #se posiciona en las coordenadas
        self.entrada_texto.config(width=50) #se le asigna el ancho
        self.entrada_texto.bind("<Return>", lambda event: self.btnEnviar(nombre, self.entrada_texto.get())) #se envia al precionar enter
        #se configura el boton enviar
        self.enviar = tk.Button(master, text="Enviar mensaje", command=lambda: self.btnEnviar(nombre, self.entrada_texto.get()))
        self.enviar.pack(pady=20)
        self.enviar.place(relx=0.700, rely=0.800)
        #se configura el boton salir
        self.boton_regresar = tk.Button(master, text="Salir", command=lambda: self.ir_a_ventana1(nombre))
        self.boton_regresar.pack(pady=20)
        self.boton_regresar.place(relx=0.500, rely=0.900)
        #CONEXION
        host = 'localhost'
        port = 55555
        #creacion del socket y conexion
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        
        #iniciamos un hilo para receive messages corra de forma simultanea
        receive_thread = threading.Thread(target=self.receive_messages, args=(self.client, nombre))
        receive_thread.start()

    def receive_messages(self, cliente, username): #se ejecuta en un hilo separado para que constantemente reciba mensajes del ciente
        try:
            while True:
                message = cliente.recv(1024).decode('utf-8') #se recibe el mensaje y se decodifica guardando en la variable message
                if message == "@username":
                    cliente.send(username.encode("utf-8"))
                else:
                    self.lista.insert(tk.END, message)
        except Exception as e:
            self.lista.insert(tk.END, f"\nHa ocurrido un error: {e}")
            cliente.close()

    def write_messages(self, username, message): #se envia el mensaje formateado al servidor
        mensaje = f"{username}: {message}"
        self.client.send(mensaje.encode('utf-8'))
        self.lista.insert(tk.END, f"        {message}")

    def btnEnviar(self, username, message): #vinculada al evento del boton enviar
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
