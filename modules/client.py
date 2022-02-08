import argparse
from socket import AF_INET, SOCK_STREAM
from modules.configuration import Configuration
import re
class Client:
    """ A class containing data to be transmitted to a Daemon
        to create and instance, use the newClient() Factory method. 
    """
    def __init__(self):
        self._action = None
        self._args = None
        self._port = None
        self._hostname = None
    
    def send(self):
        """Send() method opens a socket connection to the daemon and transmitts a action request
        """
        import socket
        import json

        s = socket.socket(AF_INET, SOCK_STREAM)
        s.connect((self._hostname, self._port))
        
        greeting = ''
        while True:
                buffer = s.recv(1024)
                if len(buffer) == 0:
                    break
                
                greeting += buffer.decode()
                if len(buffer) < 1024:
                    break 
        
        
        localport = int(re.sub('[()\',]', '', greeting).split(' ')[1])
        
        myobject = { self._action : self._args }
        s.sendall(json.dumps(myobject).encode())

        # If we send an 'add' action request, we expect the caemon to 
        # respond with a list of potential candidate titles and their
        # program descriptions.
        #
        # We will wait for the daemon to respond,  display them to the
        # user and send back a message to the daemon containing our 
        # choice if none of the candidates are what we're searching for,
        # the response will contain a None respose to terminate the 
        # thread
        if self._action == 'add':
            print('waiting for response from Daemon')

            recievedData = ''
            while True:

                buffer = s.recv(1024)
                if len(buffer) == 0:
                    break
                
                recievedData += buffer.decode()
                if len(buffer) < 1024:
                    break
            
            m = json.loads(recievedData)
            for i, show in enumerate(m['candidates']):
                for k, v in show.items():
                    print(f'[{i}] - Title: {k}\n')
                    print(f'{v}\n')
                    
            
            try:
                choice = int(input('Choose the description that matches your show (0..{} or N=None): '.format(len(m['candidates']))))
            except:
                choice = None
            else:
                if not 0 <= choice <= len(m['candidates']):
                    choice = None

            response = { 'client' : choice}
            
            s.sendall(json.dumps(response).encode())

        s.close()
        

    @classmethod
    def newClient(self, ns, hostname='localhost'):
        """Factory Method for creating Client object

        Args:
            ns (Namespace): Argparse generated Namespace
            hostname (str, optional): hostname where the Daemon is running. Defaults to 'localhost'.

        Raises:
            TypeError: ns requires an argparse.Namespace object

        Returns:
            Client: a fully configured Client object
        """
        if not isinstance(ns, argparse.Namespace):
            raise TypeError('In function newClient: ns requires an argparse.Namespace object')
        
        def createArgumentList():
            d = {}
            if ns.action == 'add':
                d = { '-t' : ' '.join(ns.t)}
                if ns.y:
                    d['-y'] = ' '.join(ns.y) 
                if ns.n: 
                    d['-n'] = ' '.join(ns.n)

            return d     

        client = Client()
        config = Configuration()
        client._action = ns.action
        client._args = createArgumentList()
        client._port = config.port
        client._hostname = hostname

        return client


