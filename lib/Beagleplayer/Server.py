import os,sys
import asyncore
import socket
import time


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
    
    _config         = None
    handlerClass    = None
    messageClass    = None
    dispatcher      = None
    
    def __init__(self, config, dispatcher=None, handlerClass=None, messageClass=None):
        self.setConfig(config)
        asyncore.dispatcher.__init__(self)
        self.createSocket(self.getHost(), self.getPort())
        #self.listen(5);
        
        if handlerClass is None:
            handlerClass = Handler
        self.handlerClass = handlerClass
        
        if messageClass is None:
            messageClass = Message.Message
        self.messageClass = messageClass
            
        self.dispatcher = dispatcher
        
    def getHost(self):
        return self._config.host
    
    def getPort(self):
        return self._config.port
        
    def createSocket(self, host, port):
        print "socket on: (%s, %s)" % (host,port)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.set_reuse_addr()
        self.bind((host, port))
        
    def handle_read(self):
         data, a = self.recvfrom(512)
         if data is not '':
             self.dispatchRequest(data, a)
        
    def setConfig(self, config):
        self._config = config
        
    def writable(self):
        return 0
    
    def handle_accept(self):
        acc = self.accept()
        if acc is None:
            pass
        else:
            sock,addr = acc
            print "connect from: %s" % (addr[0]) 
            self.handlerClass(sock, addr, self)
            
    def handle_connect(self):
        pass
        
    def handle_except(self):
        pass
    
    def handle_close(self):
        self.close()
        
    def dispatchRequest(self, data, sender):
        if self.dispatcher is None:
            return
        
        self.dispatcher.request(data, sender)
        

class Handler(asyncore.dispatcher):
    def __init__(self, sock, address, server):
        self.server = server
        self.sender = address
        self.readbuff   = ''
        self.writebuff  = ''
        
        asyncore.dispatcher.__init__(self, sock)
    
    def writable(self):
        return (len(self.writebuff) > 0)
        
    def handle_read(self):
        data, a = self.recv(1024)
        print "data: %s" % (data)
        if (data):
            self.server.dispatchRequest(data, a)
        
    def handle_write(self):
        if (len(self.writebuff) > 0):
            sent = self.send(self.writebuff)
            self.writebuff = self.writebuff[sent:]
    
    def handle_close(self):
        self.close()
        