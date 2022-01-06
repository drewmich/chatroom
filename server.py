#!/usr/bin/env python3
import socket
import threading

# Set params
host = '127.0.0.1'
port = 4334

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()
print("Chat server running on " + host + ":" + str(port)    )

clients = []
nicknames = []



# Helper to send msgs
def broadcast(msg):
    for client in clients:
        client.send(msg)

# Handle a client
def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except:
            idx = client.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[idx]
            broadcast("{} left.".format(nickname).endocde('ascii'))
            nicknames.remove(nickname)
            break

# Recieve a client
def recieve():
    while True:
        client, address = server.accept()
        print("{} connected".format(str(address)))

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname is {}".format(nickname))
        broadcast("{} joined.".format(nickname).encode('ascii'))
        client.send('Connected to server.'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

recieve()
