from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import logging

"""Module de gestion des messages et des connexions"""

class messages:
    def __init__(self, server, clients, adresses, bufsiz):
        self.server = server
        self.clients = clients
        self.adresses = adresses
        self.bufsiz = bufsiz
    def accept_incoming_connections(self):
        """Ajoute un nouveau client dans le serveur."""
        while True:
            client, client_address = self.server.accept()
            client.send(bytes("@auto_message: Bienvenue dans le serveur! Entrez un pseudo. ", "utf8"))
            self.adresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()
            logging.info('Nouveau client')

    def handle_client(self, client): 
        """Reçois le message du client et effectue un traitement sur le message"""
        
        name = client.recv(self.bufsiz).decode("utf8")
        welcome = '@auto_message: Bienvenue %s! Nous avons averti les autres participant de votre arrivé. Entrez /quit pour quitter' % name
        client.send(bytes(welcome, "utf8"))
        msg = "@auto_message: %s à rejoint le chat." % name
        self.broadcast(bytes(msg, "utf8"))
        self.clients[client] = name
                
        while True:
            msg = client.recv(self.bufsiz)
            if msg != bytes("/quit", "utf8"):
                self.broadcast(msg, "@"+name+": ")
            else:
                client.send(bytes("/quit", "utf8"))
                client.close()
                del self.clients[client]
                self.broadcast(bytes("@auto_message: %s à quitté le chat" % name, "utf8"))
                breaks


    def broadcast(self, msg, prefix=""):
        """Envoie un message à tous les clients connectés sur le serveur"""
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8")+msg)
