from operator import truediv
import socket
#import json
from modules.configuration import Configuration

class Daemon:

    def __init__(self, host='localhost'):
        self.config = Configuration()
        self.sock = socket.socket()
        self.sock.bind((host, self.config.port))
        self.sock.listen()

    def start(self):
        #log.info(f'Listening for connections on \'localhost:{self.config.port}\'')
        
        while True:
            client, address = self.sock.accept()
            client.send('Epigetd recieved your connection request'.encode())
            #log.info(f'recieved connection from {address}')
            #message = json.loads(client.recv(1500))
            #log.info(f'From: {address} Recieved: {type(message)} \'{message}\'')