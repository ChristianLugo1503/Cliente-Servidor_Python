import socket
import threading
import time

host = '192.168.1.238'
port = 55555

# Crear socket, lo llamamos server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"**** Servidor activo en {host}:{port} ****")

# Listas
clients = []       # Se almacenan las conexiones de los clientes
usernames = set()   # Cambiado a un conjunto para mejorar la eficiencia
chat_history = []   # Se almacenará el historial del chat

# Función para enviar los mensajes a todos los clientes
def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

# Función para guardar el historial del chat en un archivo de texto
def save_chat_history():
    with open('chat_history.txt', 'w') as file:
        for entry in chat_history:
            file.write(f"{entry['username']}: {entry['message']}\n")

# Función para enviar mensajes
def handle_messages(client, user):
    while True:
        try:
            message = client.recv(1024)
            if not message:  # Si no hay mensaje, el cliente se desconectó
                break
            chat_entry = {'username': user, 'message': message.decode('utf-8')}
            chat_history.append(chat_entry)
            save_chat_history()  # Guardar el historial después de cada mensaje
            broadcast(message, client)
        except:
            index = clients.index(client)
            user = list(usernames)[index]
            broadcast(f"**** {user} salió del chat ****".encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(user)
            client.close()
            break

# Función para aceptar y recibir conexiones
def receive_connections():
    while True:
        client, address = server.accept()

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.add(username)

        print(f"**** {username} se conectó desde {str(address)} ****")

        # Enviar historial del chat al nuevo cliente solo si el usuario ya estaba en el chat
        if username in usernames:
            for entry in chat_history:
                history_message = f"{entry['message']}".encode('utf-8')
                client.send(history_message)
                # Agregar un pequeño retraso para garantizar que los mensajes se reciban por separado
                time.sleep(0.1)

        message = f"**** {username} se ha unido ****".encode("utf-8")
        broadcast(message, client)
        client.send("**** Conectado al servidor ****".encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(client, username))
        thread.start()

# Cargar historial del chat al inicio del servidor
open('chat_history.txt', 'w').close()
try:
    with open('chat_history.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(': ')
            if len(parts) == 2:
                entry = {'username': parts[0], 'message': parts[1]}
                chat_history.append(entry)
except FileNotFoundError:
    pass  # El archivo no existe, lo crearemos al guardar el primer mensaje

# Limpiar historial si no hay usuarios conectados
if len(usernames) == 0:
    open('chat_history.txt', 'w').close()

# Iniciar el servidor y recibir conexiones
receive_connections()
