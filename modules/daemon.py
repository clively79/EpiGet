from operator import truediv
import socket
import json
from publisher import Publisher
from modules.configuration import Configuration


class Daemon(Publisher):

    def __init__(self, host='localhost'):
        self.config = Configuration()
        self.sock = socket.socket()
        self.sock.bind((host, self.config.port))
        self.sock.listen()

    def start(self):
        super.notifySubscribers(
            f'Listening for connections on \'localhost:{self.config.port}\'')

        while True:
            client, address = self.sock.accept()
            client.send('Epigetd recieved your connection request'.encode())
            super.notifysubscribers(f'recieved connection from {address}')
            message = json.loads(client.recv(1500))
            super.notifySubscribers(
                f'From: {address} Recieved: {type(message)} \'{message}\'')
