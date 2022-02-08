from asyncore import dispatcher
import json
import socket
import threading
from modules.messages import Dispatch, LogMessage
from modules.publisher import Publisher
from modules.subscriber import Subscriber
from modules.configuration import Configuration
from bs4 import BeautifulSoup

class ShowAdder(Publisher):
    def __init__(self):
        Publisher.__init__(self)
        self._TID = None
        self._client = None
        self._title = None
        self._year = None
        self._network = None
        self._candidates = None
        self._scheduleEntry = {
            'id' : None,
            'title' : None,
            'year' : None,
            'network' : None,
            'next episode' : {
                'url' : None,
                'subtitle' : None,
                'season' : None,
                'episode' : None
            }
        }

    @classmethod
    def newShowAdder(self, message: Dispatch):
        _object = ShowAdder()
        _object._client = message.getClient()
        args = message.getArgs()        
        _object._title = args['-t'] if '-t' in list(args) else None
        _object._year = args['-y'] if '-y' in list(args) else None
        _object._network = args['-n'] if '-n' in list(args) else None
        _object._TID =  threading.currentThread().ident
        return _object 

    def start(self):
        import requests
        def detag(html):
            soup = BeautifulSoup(html, "html.parser")
  
            for data in soup(['style', 'script']):
                data.decompose()
  
            return ' '.join(soup.stripped_strings)
        
        config = Configuration()
        self._TID = threading.currentThread().ident
        f = lambda a: f' {a}' if a else ''
        
        url = "https://tvjan-tvmaze-v1.p.rapidapi.com/search/shows"
        
        querystring = {'q': f'{f(self._title)}'}
        
        headers = {
            'x-rapidapi-host': "tvjan-tvmaze-v1.p.rapidapi.com",
            'x-rapidapi-key': config.api_key
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        self._candidates = json.loads(response.text)
        if self._year:
            i = 0
            while i < len(self._candidates):
                v = self._candidates[i]
                date = v['show']['premiered']
                y = date.split('-')[0]
                if self._year != y:
                    self._candidates.pop(i)
                    continue
                
                i+=1
        
        if self._network:
            i = 0
            while i < len(self._candidates):
                v = self._candidates[i]
                n = str(v['show']['network']['name']).lower()
                if str(self._network).lower() != n:
                    self._candidates.pop(i)
                    continue
                
                i+=1
        
        m = {'candidates' : [] }
        
        for v in self._candidates:
            m['candidates'].append(  { v['show']['name'] : detag(v['show']['summary']) } ) 
             
        self._client.sendall(json.dumps(m).encode())
        threading.current_thread().setName(f'{self._title} -  Waiting for Client')       
        self.notifySubscribers(LogMessage.newLogMessage('Scrape complete, waiting for response from client'))
        
        recievedData = ''
        while True:

            buffer = self._client.recv(1024)
            if len(buffer) == 0:
                break
            
            recievedData += buffer.decode()
            if len(buffer) < 1024:
                break
        
        clientsChoice = json.loads(recievedData)['client']
        if isinstance(clientsChoice, int):
            self.notifySubscribers(LogMessage.newLogMessage(f'Client chose candidate: {clientsChoice}'))
        else:
            self.notifySubscribers(LogMessage.newLogMessage(f'Client chose none to the candidates'))

    def get_TID(self) -> int:
        return self._TID
    


     