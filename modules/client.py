import argparse
import sys
from modules.configuration import Configuration
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

        s = socket.socket()
        s.connect((self._hostname, self._port))
        myobject = { self._action : self._args }
        s.send(json.dumps(myobject).encode())
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


