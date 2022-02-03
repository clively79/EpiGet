import sys
import socket
import json
from modules.configuration import Configuration
from modules.subscriber import Subscriber
from modules.publisher import Publisher
from modules.subscriber import Subscriber
from modules.log import DaemonLogger
class Daemon(Publisher):
    """Listens for connections, recieves data from client connections, and notifies worker threads for various tasks

    Args:
        Publisher (Publisher): Aloows Subscriber objects to be notified of state changes 
    """
    def __init__(self, cfg, host='localhost'):
        """ctor

        Args:
            cfg (Configuration): A configuration object containing user defined settings used by the Daemon
            host (str, optional): Host address of the machine where the daemon is running. Defaults to 'localhost'.

        Raises:
            TypeError: if the cfg argument is not a Configuration ofject a TypeError exception is raised
        """
        Publisher.__init__(self)
        if not isinstance(cfg, Configuration):
            raise TypeError
            
        self.config = cfg
        self.sock = socket.socket()
        self.sock.bind((host, self.config.port))
        self.sock.listen()
        self.threads = set()
        self.logger = DaemonLogger()
        

    def start(self):
        """Starts the daemon.
        """
        self.addSubscriber(self.logger)
        self.notifySubscribers({'log': [f'Listening for connections on \'localhost:{self.config.port}\'']})
        while True:
            client, address = self.sock.accept()
            self.notifySubscribers({'log': [f'recieved connection from {address}']})
            try:
                data = json.loads(client.recv(1500))
            
            except:
                self.notifySubscribers({'log': [f'Malformed Message from {address}']})
                
            else:
                self.notify(data)


            
    
        

        
