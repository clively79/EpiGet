#!/usr/bin/python3

import sys
import os
import logging
from modules.configuration import Configuration
from modules.daemon import Daemon


def main():
    logging.basicConfig(filename='epiget.log',
                        format='[EPIGET DAEMON][%(asctime)s %(message)s]',
                        filemode='a')
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    daemon = Daemon()
    daemon.start()

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
            
