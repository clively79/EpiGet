#!/usr/bin/python3

import sys
import socket
import json
import os
import logging
from modules.configuration import Configuration


def main():
    logging.basicConfig(filename='epiget.log',
                        format='[EPIGET DAEMON][%(asctime)s %(message)s]',
                        filemode='a')
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    PID = os.getpid()
    config = Configuration()

    sock = socket.socket()
    sock.bind(('localhost', config.port))
    sock.listen()
    
    log.info(f'Started with PID: {PID} Listening for connections on \'localhost:{config.port}\'')
    
    while True:
        client, address = sock.accept()
        client.send('Epigetd recieved your connection request'.encode())
        log.info(f'recieved connection from {address}')
        message = json.loads(client.recv(1500))
        log.info(f'From: {address} Recieved: {type(message)} \'{message}\'')


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
                main()
            
