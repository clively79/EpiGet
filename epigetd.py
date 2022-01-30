import sys
import socket
import json
import multiprocessing
import os
from modules.configuration import Configuration


def main():
    print(f'EpiGet Daemon running with PID {os.getpid()}')
    settings = open('config.json', 'r')
    config = Configuration(json.loads(settings.read()))
    settings.close()
    sock = socket.socket()
    sock.bind(('localhost', config.port))
    sock.listen()

    while True:
        client, address = sock.accept()
        print(f'recieved connection from {address}')
        data = client.recv(1500)
        message = bytes(data)
        print(json.loads(message.decode()))


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
            PID = os.getpid()
            print(f'parent Process\'s PID is {os.getpid()}')
            daemon = multiprocessing.Process(target=main)
            daemon.start()
