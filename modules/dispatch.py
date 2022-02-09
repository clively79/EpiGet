

from socket import socket
import string
from modules.messages import *
from modules.publisher import Publisher
from modules.scraper import ShowAdder
from modules.subscriber import Subscriber
import threading


""" The Dispatcher class runs as a background thread and listens for new messages
    when a publisher that the dispatcher has subscribed to sends a message
    the message is examined for type.  
    
    If the message is a Dispatch type,
    it is appended to the dispatherMessages queue and a set() signal is sent to 
    the dispatchEvent to wake up the thread if it is sleeping.

    If the message is not a WorkOrder type,  it is ignored and discarded 
"""
class Dispatcher(Subscriber, Publisher):
    """The Dispather class is a singleton. Only one object may be instantiated 
    from the class.  If an attempt is made to instatiate a second instance,  a 
    reference to the existing instance will be returned. 

    The Dispatcher class runs as a background thread and listens for new messages
    when a publisher that the dispatcher has subscribed to sends a message
    the message is examined for type.  
    
    If the message is a Dispatch type,
    it is appended to the dispatherMessages queue and a set() signal is sent to 
    the dispatchEvent to wake up the thread if it is sleeping.

    If the message is not a WorkOrder type,  it is ignored and discarded

    Args:
        Subscriber (Abstract Class): 
            Abstract: notify()
        
        Publisher (Concrete Class): 
            var subscribers: set() init empty
            notifySubscribers(self, message)
            addSubscriber(self, member)
            removeSubscriber(self, member)
    
    Returns:
        Dispatcher: Object

    """
    
    _instance = None

    def __init__(self):
        Publisher.__init__(self)
        self._dispatchMessages = []
        self._threads = {} 
        self._dispatchEvent = threading.Event()
        self._dispatcherMessageLock = threading.Lock()
        self._thread = threading.Thread(target=self.dispatcherThread)
        self._thread.start()

    @classmethod
    def instance(self):
        return self._instance
        
    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)

        return cls._instance

    def get_TID(self):
        return self._thread.ident

    def notify(self, req):
        if isinstance(req, Dispatch):
            self._dispatcherMessageLock.acquire()
            self._dispatchMessages.append(req)
            self._dispatcherMessageLock.release()
            self._dispatchEvent.set()
            self._dispatchEvent.clear()
        
        if isinstance(req, LogMessage):
            self.notifySubscribers(req)

    def dispatcherThread(self):
        
        switch = {
            'add' : self.add,
            'delete' : self.deleteShow,
            'terminate' : self.terminateThread
        }

        while True:
            
            # If there are no messages for the dispatcher thread to handle
            # sleep until someone sets the dispatch event. 
            # We Don't do busy-waiting here
            if not self._dispatchMessages:
                 self._dispatchEvent.wait()
            
            # continue processing dispatch messages as long as there are
            # messages in the dispatchMessages queue.
            if self._dispatchMessages:
                self._dispatcherMessageLock.acquire()
                message = self._dispatchMessages.pop(0)
                self._dispatcherMessageLock.release()
            
                
                action = message.getAction()
                 
                switch[action](message)
                #self.notifySubscribers(LogMessage.newLogMessage(f'Action requested by the client could not be performed {action}'))
    
    def add(self, m: Dispatch):
        args = m.getArgs()        
        title = args['-t'] if '-t' in list(args) else None
        year = args['-y'] if '-y' in list(args) else None
        network = args['-n'] if '-n' in list(args) else None
        f = lambda a: ', ' + a if a else ''
        s = f'Client requested to add {title}{f(year)}{f(network)}, Launching scraper thread'
        self.notifySubscribers(LogMessage.newLogMessage(s))
        scraper = ShowAdder.newShowAdder(m)
        scraper.addSubscriber(self)
        newThread = threading.Thread(target=scraper.start, name=title)
        newThread.start()
        self._threads[str(newThread.ident)] = scraper

    def terminateThread(self, m: Dispatch):
        self._threads.pop(str(m.getTID()))


    def deleteShow(self, **args):
        pass