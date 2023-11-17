import socket   
import threading

host = 'localhost'
port = 55555

#crear socket lo llamamos server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port)) #le pasamos los datos de conexión
server.listen()
print(f"**** Servidor activo en {host}:{port} ****")

#listas
clients = [] #se almacenan las conexiones de los uclientes
usernames = [] # se almacenan los usernames de los clientes

#Funcion para enviar los mensajes a todos los clientes
def broadcast(message, _client): # envia el mensaje a todos los clientes menos al que lo envio
    for client in clients: #recorremos la lista
        if client != _client: #si el cliente no es igual a el mismo, envia el mensaje
            client.send(message)

#Funcion para enviar mensajes
def handle_messages(client): 
    while True:
        try:
            message = client.recv(1024) #obtenemos el mensaje
            broadcast(message, client) #se lo envia al broadcast para distribuirlo
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"**** {username} salió del chat ****".encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break
        
#Funcion para aceptar y recibir conexiones
def receive_connections():
    while True:
        client, address = server.accept() #aceptamos la conexion de cliente

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"**** {username} se conectó desde {str(address)} ****") #al conectarse el usuario imprime el mensaje

        message = f"**** {username} se ha unido ****".encode("utf-8") # este mensaje se enviara por el broadcast
        broadcast(message, client)
        client.send("**** Conectado al servidor ****".encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

receive_connections()
