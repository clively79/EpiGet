import sys
import socket
import json
import os
import datetime
from modules.configuration import Configuration


def main():

    while True:
        client, address = sock.accept()
        logfile.write(f'[EpiGet Daemon] [{datetime.now()}] recieved connection from {address}')
        data = client.recv(1500)
        message = bytes(data)
        logfile.write(f'[EpiGet Daemon] [{datetime.now()}] {address} sent \'{json.loads(message.decode())}\'')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--configure':
        Configuration.configure()
    else:
        try:
            settings = open('config.json', 'r')
        except:
            print(
                "EpiGet has not been configured. Run 'epiget.py --configure' before using EpiGet.")
        else:
            settings.close()
            PID = os.fork()
            if PID == 0:
                sys.exit(0)
            else:
                settings = open('config.json', 'r')
                config = Configuration(json.loads(settings.read()))
                settings.close()
                sock = socket.socket()
                sock.bind(('localhost', config.port))
                sock.listen()
                logfile = open('epiget.log', 'a')
                logfile.write(f'[EpiGet Daemon] [{datetime.now()}] Started with PID: {PID} Listening for connections on \'localhost:{config.port}\'')
                main()
            
