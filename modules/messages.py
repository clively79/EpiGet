from socket import socket


""" class Message:
    def __init__(self):
        self._catalogue = {}
    
    def has(self, t):
        return True if t in self._catalogue else False
    
    def get(self, t):
        return self._catalogue[str(type(t))] if self.has(t) else None """

class Dispatch():
    _actions = ['add', 'delete', 'send', 'forward']
    
    def __init__(self) -> None:
        self._m = { 
            'dispatcher'    : {
                'action'    : None,
                'client'    : None,
                'tid'       : None,
                'message'   : {}
            }
        }
        
    @classmethod
    def newDispatch(self, action, client, tid=None, **kwargs):
           
        if not action \
            or not isinstance(action, str) \
            or not isinstance(client, socket) \
            or action not in self._actions:
            return None
           
        obj = Dispatch()
        obj._m['dispatcher']['action'] = action
        obj._m['dispatcher']['client'] = client
        if tid:
            obj._m['dispatcher']['tid'] = tid

        for k, v in kwargs.items():
            obj._m['dispatcher']['message'][k] = v

        return obj

    def getAction(self):
        return self._m['dispatcher']['action']
    
    def getClient(self):
        return self._m['dispatcher']['client']
    
    def getArgs(self):
        return self._m['dispatcher']['message']
    
    def getTID(self):
        return self._m['dispatcher']['tid']
class LogMessage():
    def __init__(self) -> None:
        self._m = '' 
        
    @classmethod
    def newLogMessage(self, m):
        
        me = LogMessage()    

        
        if isinstance(m, str):
            me._m = m

        return me

    def get(self):
        return self._m
