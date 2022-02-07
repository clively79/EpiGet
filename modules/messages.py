from socket import socket


class Message:
    def __init__(self):
        self._catalogue = {}
    
    def has(self, t):
        return True if t in self._catalogue else False
    
    def get(self, t):
        return self._catalogue[str(type(t))] if self.has(t) else None

class Dispatch(Message):
    def __init__(self) -> None:
        Message.__init__(self)
        self._client = None
        self._m = None
        
    @classmethod
    def newDispatch(self, payload, client=None):
        
        me = Dispatch()    
        me._catalogue[me.__class__.__name__] = self

        if isinstance(payload, dict):
            me._client = client
            me._m = payload
        
        return me

    def getClient(self):
        return self._client
    
    def getPayload(self):
        return self._m

class LogMessage(Message):
    def __init__(self) -> None:
        Message.__init__(self)
        self._m = '' 
        
    @classmethod
    def newLogMessage(self, m):
        
        me = LogMessage()    
        me._catalogue[me.__class__.__name__] = self
        
        if isinstance(m, str):
            me._m = m

        return me

    def get(self):
        return self._m

    
