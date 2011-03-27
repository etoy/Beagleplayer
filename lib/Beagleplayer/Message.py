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
    """
        reg = re.compile('(c|e)\:([0-9]{1,2})\:([0-9]{1,2})\:([a-zA-Z0-9]+)', re.IGNORECASE)
        m = reg.match(str)
        if (m is not None):
            self.setType(m.group(1).strip())
            self.setSender(m.group(2).strip())
            self.setDest(m.group(3).strip())
            self.setMessage(m.group(4).strip())
    """

class PlayerMessage(Message):
    def __init__(self):
        Message.__init__(self)