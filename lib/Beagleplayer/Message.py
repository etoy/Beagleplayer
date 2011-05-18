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
            
    def parseTamatarMsg(self, str):
        reg = re.compile()
        
        
        
"""
    Message format: <type>:<sender>:<destination>:<cmd>
"""

class TamatarMessage(Message):
    
    def toString(self):
        return "%s:%s:%s:%s" % (self.getType(), self.getSender(), self.getDest(), self.getMessage())
        
    def parse(self, str):
        reg = re.compile('(c|e)\:([0-9]{1,2})\:([0-9]{1,2})\:([a-zA-Z0-9]+)', re.IGNORECASE)
        m = reg.match(str)
        if (m is not None):
            self.setType(m.group(1).strip())
            self.setSender(m.group(2).strip())
            self.setDest(m.group(3).strip())
            self.setMessage(m.group(4).strip())
            
    def isSoundCommand(self):
        scmd = self.getSoundCommand()
        if scmd is not None:
            return True
        return False
        
    def getSoundCommand(self):
        reg = re.compile('s([0-9]+|stop|all)', re.IGNORECASE)
        m = reg.match(self.getMessage())
        if m is not None:
            return m.group(1).strip()
            
        return None
   