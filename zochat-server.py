"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import logging
import messages

# Configuration du système de log
logging.basicConfig(level=logging.INFO)

port = input('Entrez un port pour votre serveur  [31000] : ')
if port == "":
    port = 31000
else:
    port = int(port)
PORT = port

HOST = '0.0.0.0'
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(
    AF_INET,
    SOCK_STREAM)

SERVER.bind(ADDR)

messages_app = messages.messages(server=SERVER,
                                 clients={},
                                 adresses={},
                                 bufsiz=BUFSIZ)

if __name__ == "__main__":
    logging.info('En attente de connexion...')
    SERVER.listen(5)
    ACCEPT_THREAD = Thread(target=messages_app.accept_incoming_connections)
    
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
