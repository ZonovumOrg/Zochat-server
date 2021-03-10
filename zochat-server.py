"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import logging

# Configuration du système de log
logging.basicConfig(level=logging.INFO)

port = input('Entrez un port pour votre serveur  [31000] : ')
if port == "":
    port = 31000
else:
    port = int(port)
PORT = port

def accept_incoming_connections():
    
    """Ajoute un nouveau client dans le serveur."""
    while True:
        client, client_address = SERVER.accept()
        client.send(bytes("@auto_message: Bienvenue dans le serveur! Entrez un pseudo. ", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()
        logging.info('Nouveau client')

def handle_client(client):  # Takes client socket as argument.
    """Reçois le message du client et effectue un traitement sur le message"""

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
            broadcast(bytes("@auto_message: %s à quitté le chat" % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Envoie un message à tous les clients connectés sur le serveur"""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)
clients = {}
addresses = {}

HOST = '0.0.0.0'
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    logging.info('En attente de connexion...')
    SERVER.listen(5)
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
