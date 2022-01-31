from abc import abstractmethod
from operator import truediv
import socket
import json
from modules.subscriber import Subscriber
from modules.publisher import Publisher
from modules.subscriber import Subscriber
from modules.configuration import Configuration       
from modules.messagetypes import *
#import threading 

class Daemon(Publisher, Subscriber):

    def __init__(self, host='localhost'):
        Publisher.__init__(self)
        self.config = Configuration()
        self.sock = socket.socket()
        self.sock.bind((host, self.config.port))
        self.sock.listen()
        self.messages = []


    def start(self):
        self.notifySubscribers(
            f'Listening for connections on \'localhost:{self.config.port}\'')

        while True:
            client, address = self.sock.accept()
            client.send('Epigetd recieved your connection request'.encode())
            self.notifySubscribers(f'recieved connection from {address}')
            message = json.loads(client.recv(1500))
            self.notifySubscribers(
                f'From: {address} Recieved: {type(message)} \'{message}\'')

    def notify(self, message):
        if message.isinstance(DaemonMessage):
            self.messages.push(message)
