import os,sys
import asyncore
import socket
import time

import Message

class NullDevice:
    logfile = None
    def __init__(self, l):
        self.logfile = l
    
    def write(self, s):
        self.logfile.write(s)
        self.logfile.flush()


def becomeDaemon(ourHomeDir, logfile):
        if os.fork() != 0:
            os._exit(0)
        os.setsid()
        os.chdir(ourHomeDir)
        os.umask(0)
        sys.stdin.close()
        for z in range(0, 256):
            try:
                os.close(z)
            except:
                pass    

        os.open('/dev/null', os.O_RDWR)
        sys.stdout = sys.stderr = NullDevice(open(logfile, 'a+'))
        
def createPidfile(pidfile):
    try:
        f = open(pidfile, 'w')
        f.write(str(os.getpid()).strip())
        f.close()
    except IOError as (errno, strerror):
        print "Creating pidfile failed: %s" % (strerror)
    
        
class Listener(asyncore.dispatcher):
    
    _config = None
    _ip     = ''
    _broker = None
    
    def __init__(self, config):
        self.setConfig(config)
        asyncore.dispatcher.__init__(self)
        self.createSocket(self.getHost(), self.getPort())
        asyncore.dispatcher.set_reuse_addr(self)
        self.setIp(socket.gethostbyname(socket.gethostname()))
        #self.setBroker(broker) 
        
    def setBroker(self, broker):
        self._broker = broker
        
    def getBroker(self):
        return self._broker
        
    def setIp(self, ip):
        self._ip = ip
        
    def getHost(self):
        return self._config.host
    
    def getPort(self):
        return self._config.port
        
    def createSocket(self, host, port):
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind((host, port))
        
    def handle_read(self):
        print "reading ... "
        data, a = self.recvfrom(512)
        
        if data != '':
            msg = TamatarMessage.Message()
            msg.parse(data)
            msg.setSenderHostPort(a)
            br = self.getBroker()
            if (br is not None):
                br.addMessageIn(msg)
            
        print "addr: ", self._ip
        print data, a
        
    def setConfig(self, config):
        self._config = config
        
    def writable(self):
        return 0
    
    def handle_accept(self):
        pass
    
    def handle_connect(self):
        pass
        
    def handle_except(self):
        pass
    
    def handle_close(self):
        self.close()
        
