import argparse
import sys
from modules.configuration import Configuration
class Client:
    """ A class containing data to be transmitted to a Daemon
        to create and instance, use the newClient() Factory method. 
    """
    def __init__(self):
        self._key = None
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
        myobject = { self._key : self._args }
        s.send(json.dumps(myobject).encode())
        s.close()

    @classmethod
    def newClient(self, args, hostname='localhost'):
        """Factory Method for creating Client object

        Args:
            args (Namespace): Argparse generated Namespace
            hostname (str, optional): hostname where the Daemon is running. Defaults to 'localhost'.

        Raises:
            TypeError: args requires an argparse.Namespace object

        Returns:
            Client: a fully configured Client object
        """
        if not isinstance(args, argparse.Namespace):
            raise TypeError('In function newClient: args requires an argparse.Namespace object')
        
        def createArgumentList() -> list:
            
            l = [args.action]
            if args.action == 'add':
                l.append('-t')
                l.append(' '.join(args.t))
                if args.y:
                    l.append('-y')
                    l.append(' '.join(args.y))
                if args.n:
                    l.append('-n')
                    l.append(' '.join(args.n))

            if args.action == 'delete':
                l.append('-id')
                l.append(args.id)
            
            return l

        client = Client()
        config = Configuration()
        client._key = sys.argv[0]
        client._args = createArgumentList()
        client._port = config.port
        client._hostname = hostname

        return client


    