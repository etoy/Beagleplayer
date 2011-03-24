import re

class Message():
    
    _msg            = ''
    _sender         = 0
    _dest           = 0
    _type           = ''
    _senderhostport = ()
    
    def __init__(self):
        pass
    
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
    
    def setSenderHostPort(self, hp):
        self._senderhostport = hp
        
    def getSenderHostPort(self):
        return self._senderhostport
    
    def setDestHostPort(self, hp):
        self._desthostport = hp
        
    def getDestHostPort(self):
        return self._desthostport
    
    def parse(self, str):
        reg = re.compile('(c|e)\:([0-9]{1,2})\:([0-9]{1,2})\:([a-zA-Z0-9]+)', re.IGNORECASE)
        m = reg.match(str)
        if (m is not None):
            self.setType(m.group(1).strip())
            self.setSender(m.group(2).strip())
            self.setDest(m.group(3).strip())
            self.setMessage(m.group(4).strip())
            
            
    def isCommand(self):
        if self.getType() == 'c':
            return True
        return False
            
    def isModeCommand(self):
        mcmd = self.getModeCommand()
        if mcmd is not None:
            return True
        return False
    
    # MP -> mode play 
    # MS -> mode sleep 
    # MA -> mode audio
    # MM -> manual
    def getModeCommand(self):
        reg = re.compile('m([a-z]+)', re.IGNORECASE)
        m = reg.match(self.getMessage())
        if m is not None:
            return m.group(1)
        
        return None
        
            
    def isSoundCommand(self):
        scmd = self.getSoundCommand()
        if scmd is not None:
            return True
        return False
        
    def getSoundCommand(self):
        reg = re.compile('s([0-9]+)', re.IGNORECASE)
        m = reg.match(self.getMessage())
        if m is not None:
            return m.group(1)
            
        return None
        
    def isPingCommand(self):
        if (self.getMessage() == 'ping'):
            return True
        return False
       

class CtrlMessage():
    _msg = {}

    def __init__(self, prms={}):
        self.setParams(prms)

    def setPower(self, pwr):
        self._msg['power'] = pwr
    def setUptime(self, utime):
        self._msg['uptime'] = utime
    def setId(self, id):
        self._msg['tamatarId'] = id
    def setIp(self, ip):
        self._msg['ip'] = ip
    def setState(self, state):
        self._msg['state'] = state
    
    def setParams(self, prms):
        self._msg.update(prms)
    
    def toQueryStr(self):
         q = "&".join(["%s=%s" % (f,str(v)) for f,v in self._msg.items()])
         return q
