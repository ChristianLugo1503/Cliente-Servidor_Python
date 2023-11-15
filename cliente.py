import socket
import threading

def send(sock,addr):
   '''
   Esta función acepta un socket y una tupla (dirección, puerto)
       Puede obtener la entrada del usuario a través de input () y enviar la información al socket
   '''
   while True:
      # Obtener la entrada del usuario
      string = input()
      # Enviar información de entrada
      message = name + ": " + string
      sock.sendto(message.encode('utf-8'),addr)
      # El usuario ingresa a salir para salir del chat
      if string == '--EXIT':
         break

def recv(sock,addr):
   '''
       Esta función acepta un socket y una tupla (dirección, puerto)
       La información enviada por el servidor se puede recibir a través del socket
   '''
   sock.sendto(name.encode('utf-8'),addr)
   while True:
      data = sock.recv(1024)
      print(data.decode('utf-8'))
    
    
print('____WELCOME____\n'+'EXIT -> exits\nUSERLIST -> get users')
# Obtener nombre de usuario
name = input('please input your name:')
# Crea un enchufe
socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# La dirección IP del servidor es 192.168.218.17, el puerto está configurado en 8080
server = ('localhost',8080)
# Recepción y envío multiproceso
tr = threading.Thread(target=recv,args=(socket,server),daemon=True)
ts = threading.Thread(target=send,args=(socket,server))
tr.start()
ts.start()
ts.join()
socket.close()
