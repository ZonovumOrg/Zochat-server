"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

print('Loading server... ')
port = input('Please enter port for server [31000] : ')
if port == "":
    port = 31000
else:
    port = int(port)
PORT = port

print('Vérification des connexion... ')
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print('[!] Nouveau client connecté. ')
        client.send(bytes("@auto_message: Bienvenue dans le serveur! Entrez un pseudo. ", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

print('Vérification des clients... ')
def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = '@auto_message: Bienvenue %s! Nous avons averti les autres participant de votre arrivé. Entrez /quit pour quitter' % name
    client.send(bytes(welcome, "utf8"))
    msg = "@auto_message: %s à rejoint le chat." % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("/quit", "utf8"):
            broadcast(msg, "@"+name+": ")
        else:
            client.send(bytes("/quit", "utf8"))
            client.close()
            del clients[client]
            print('[!] Client déconécté. ')
            broadcast(bytes("@auto_message: %s has left the chat." % name, "utf8"))
            break

print('Vérification du système d\'envoie...')
def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

print('Finitions... ')
clients = {}
addresses = {}

HOST = '0.0.0.0'
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    print('Server running. ')
    SERVER.listen(5)
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    try:
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    except:
        broadcast('ERROR: le serveur à eu un problème interne. Vous n\'aurez pas de réponse si vous envoyez un message. ')
    broadcast("ERROR: Le serveur à planté.")
    SERVER.close()
    print('Server closed. ')
