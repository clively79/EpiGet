from modules.subscriber import Subscriber

import logging

class DaemonLogger(Subscriber):
    """A logger intended to subscribe to the daemon for writing state information to the log file

    Args:
        Subscriber (Subscriber): Inherits the subscriber abstract class, implents the notify() method
    """
    logging.basicConfig(filename='epiget.log',
                        format='[EPIGET DAEMON][%(asctime)s %(message)s]',
                        filemode='a')
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    def notify(self, m):
        if isinstance(m, Message) and m.getMessageType() == 'log':
            self.log.info(m.getMessage())