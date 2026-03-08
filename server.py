#------------------------------------------------------------------------
# CHAT APPLICATION - Server
#------------------------------------------------------------------------
import socket
import threading
from datetime import datetime

HOST = "localhost"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
names = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            time = datetime.now().strftime("%H:%M")

            formatted = f"[{time}] {message.decode()}"
            broadcast(formatted.encode())

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            name = names[index]
            leave_msg = f"{name} left the chat"
            broadcast(leave_msg.encode())

            names.remove(name)
            break

def receive():
    print("Server is running...")

    while True:
        client, address = server.accept()
        print("Connected with", address)

        client.send("NAME".encode())
        name = client.recv(1024).decode()

        names.append(name)
        clients.append(client)

        join_msg = f"{name} joined the chat"
        broadcast(join_msg.encode())

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()
