import json
from socket import AF_INET, SOCK_STREAM, socket
from modules.messages import *
from modules.dispatch import Dispatcher
from modules.configuration import Configuration
from modules.publisher import Publisher
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
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((host, self.config.port))
        self.sock.listen()
        self.threads = {}
        self.logger = DaemonLogger()
        self.dispatcher = Dispatcher()
        self.addSubscriber(self.dispatcher)
        self.dispatcher.addSubscriber(self.logger)
        self.addSubscriber(self.logger)
        self.notifySubscribers(LogMessage.newLogMessage(f'Listening for connections on \'localhost:{self.config.port}\''))
    
    def start(self):
        """Starts the daemon.
        """
        
        
        while True:
            c, address = self.sock.accept()
            c.sendall(str(address).encode())
            self.notifySubscribers(LogMessage.newLogMessage(f'recieved connection from {address}'))
            buffer = ''
        
            while True: 
                incomming = c.recv(1024)
                buffer += incomming.decode()
        
                if len(incomming) == 0 or len(bytes(incomming)) < 1024:
                    break


            data = json.loads(buffer)
            
            # if the data is a dictionary lock dispatcher message queue
            # append the message into the queue and signal the dispatcher
            # to wake up if it is waiting for new messages
            if isinstance(data, dict):
                a = (list(data))[0]
                m = data[a]
                self.notifySubscribers(Dispatch.newDispatch(action=a, client=c, **m))


    
            
        

        
