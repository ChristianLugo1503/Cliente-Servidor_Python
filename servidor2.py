import socket   
import threading
import datetime
import os
import signal
import sys

host = '127.0.0.1'
port = 55555

# crear socket lo llamamos server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))  # le pasamos los datos de conexión
server.listen()
print(f"{'*' * 4} Servidor activo en {host}:{port} {'*' * 4}")

# listas
clients = []  # se almacenan las conexiones de los clientes
usernames = []  # se almacenan los usernames de los clientes

# Funcion para enviar los mensajes a todos los clientes
def broadcast(message, _client):  # envia el mensaje a todos los clientes menos al que lo envio
    for client in clients:  # recorremos la lista
        if client != _client:  # si el cliente no es igual a el mismo, envia el mensaje
            client.send(message)

# Funcion para manejar los mensajes y guardarlos en un archivo de texto
def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)  # obtenemos el mensaje

            # Obtener la marca de tiempo actual
            timestamp = datetime.datetime.now().strftime("%d%m%Y_%H-%M-%S")

            # Ruta al escritorio
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            file_path = os.path.join(desktop_path, f"chat_{timestamp}.txt")

            # Guardar el mensaje en el archivo
            with open(file_path, "a") as file:
                file.write(f"[{timestamp}] Message from {usernames[clients.index(client)]}: {message.decode('utf-8')}\n")

            broadcast(message, client)  # enviar el mensaje al broadcast para distribuirlo
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"{'*' * 4} {username} salió del chat {'*' * 4}".encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break

# Funcion para guardar el chat al detener el servidor
active = True

# La función para guardar el chat si no hay clientes conectados
def save_chat():
    if not clients:  # Si no hay clientes conectados
        # Obtener la marca de tiempo actual
        timestamp = datetime.datetime.now().strftime("%d%m%Y_%H-%M-%S")

        # Ruta al escritorio
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop_path, f"chat_{timestamp}.txt")

        # Guardar el chat en un archivo de texto
        with open(file_path, "w") as file:
            for i in range(len(usernames)):
                file.write(f"[{timestamp}] {usernames[i]}: se ha salido del chat\n")
# Funcion para aceptar y recibir conexiones
def receive_connections():
    while True:
        client, address = server.accept()  # aceptamos la conexion de cliente

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"{'*' * 4} {username} se conectó desde {str(address)} {'*' * 4}")  # al conectarse el usuario imprime el mensaje

        message = f"{'*' * 4} {username} se ha unido {'*' * 4}".encode("utf-8")  # este mensaje se enviara por el broadcast
        broadcast(message, client)
        client.send("{'****'} Conectado al servidor {'****'}".encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

# Capturar la señal de interrupción (Ctrl+C) para guardar el chat antes de salir
def signal_handler(sig, frame):
    global active
    active = False
    save_chat()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# La función para recibir conexiones se ajusta para comprobar si el servidor está activo
def receive_connections():
    global active
    while active:
        client, address = server.accept()
        # Resto del código...
    else:
        save_chat()  # Si no hay clientes activos, guardar el chat antes de salir

receive_connections()
