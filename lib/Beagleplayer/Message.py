import re

class Message():
    
    _msg            = ''
    _sender         = ()
    _dest           = 0
    _type           = ''
    
    
    def __init__(self):
        pass
    
    def fromString(self, inp):
        self._msg = inp
        self.parse(self._msg)
        
    def setMessage(self, msg):
        self._msg = msg.strip()
        
    def getMessage(self):
        return self._msg
    
    def setSender(self, sender):
        self._sender = sender
        
    def getSender(self):
        return self._sender
        
    def setType(self, type):
        self._type = type
        
    def getType(self):
        return self._type
        
    def setDest(self, dest):
        self._dest = dest
        
    def getDest(self):
        return self._dest
    
    def parse(self, str):
        pass
    

class PlayerMessage(Message):
    command = None
    value   = None
    def __init__(self):
        Message.__init__(self)
    
    def parse(self, str):
        reg = re.compile('^([a-z]+)(\:([a-z0-9]+))?', re.IGNORECASE)
        m = reg.match(str)
        if m is not None:
            c = m.group(1)
            if c is not None and c is not '':
                self.command = c.strip()
            v = m.group(3)
            if v is not None:
                self.value = v.strip()
            
            
        
        