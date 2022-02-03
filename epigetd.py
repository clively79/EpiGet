#!/usr/bin/python3

import sys
import os
from modules.configuration import Configuration

if __name__ == '__main__':
    try:
        settings = open('config.json', 'r')
        settings.close()
    except:
        print(
            "EpiGet has not been configured. Run 'epiget.py configure' before using EpiGet.")
    
    config = Configuration()
    if len(sys.argv) == 1:  
        
        PID = os.fork()
        if PID == 0:
            sys.exit(0)
        else:
            from modules.log import DaemonLogger
            from modules.daemon import Daemon
            
            daemon = Daemon(config)
            daemon.start()

    else:
        from modules.client import Client
        from modules.arguments import verifyArguments
        
        parsedArguments = verifyArguments()
        def printLicense():
            file = open('LICENSE', 'r')
            print(file.read())
            file.close()
        
        def printReadme():
            file = open('README', 'r')
            print(file.read())
            file.close()
        
        def launchClient():
            client = Client.newClient(parsedArguments)
            client.send()

        switch = {
                    'configure' : Configuration.configure,
                    'license'   : printLicense,
                    'readme'    : printReadme,
                    'add'       : launchClient,
                    'delete'    : launchClient,
                    'stop'      : launchClient
                }
        
        switch[parsedArguments.action]()
        
            
