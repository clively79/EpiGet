from modules.subscriber import Subscriber


import logging

class DaemonLogger(Subscriber):
     
    logging.basicConfig(filename='epiget.log',
                        format='[EPIGET DAEMON][%(asctime)s %(message)s]',
                        filemode='a')
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    def notify(self, message):
        self.log.info(message)