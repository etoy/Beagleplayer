import mplayer
import socket
import os

from Message import PlayerMessage, TamatarMessage

class Player():
    _id     = 0
    _client = None
    _libraryFile = '/home/root/audio/playlist.txt'
    _library = []

    def __init__(self, library=None, id=None):
        self._setupClient()
        if id is not None:
            self.setId(id)
        if library is not None:
            self._libraryFile = library
        self._loadLibrary()
        

    def __del__(self):
        if (self._client is not None):
            self._client.close()
    
    def getId(self):
        return self._id
    
    def setId(self, id):
        self._id = id
    
    def _loadLibrary(self):
        if os.path.isfile(self._libraryFile):
            try:
                fh = open(self._libraryFile, 'r')
                self._library = [l.strip() for l in fh.readlines()]
                
            except IOError as (errno, errmsg):
                print "failed opening library: '%s'" % (errmsg)
                return False
        return True
    
    def _setupClient(self):
        self._client = mplayer.Player()
        return True

    def isAlive(self):
        return (self._client is not None and self._client.is_alive())

    def request(self, payload, sender):
        print "got request! '%s'" % (payload)
        msg = self.parseRequest(payload, sender)
        if msg.getDest() != self.getId():
            return
        
        snd = msg.getSoundCommand()
        if snd is None:
            return
        
        self.play(snd)
        
    def parseRequest(self, payload, sender):
        # TamatarMessage
        msg = TamatarMessage()
        msg.fromString(payload)
        return msg
        
        
    def loop(self, val=0):
        if self.isAlive():
            self._client.loop = val;
            
    def playList(self, file, append=0):
        if self.isAlive():
            out = self._client.loadlist(file, append)
        
    def playFile(self, file, append=0):
        if self.isAlive():
            out = self._client.loadfile(file, append)
        
    def play(self, index):
        f = int(index)
        if f >= 0 and f < len(self._library):
            return self.playFile(self._library[f])

    def playLibrary(self):
        if (os.path.isfile(self._libraryFile)):
            self.playList(self._libraryFile)
    
    def stop(self):
        if (self.isAlive()):
            self._client.stop()
        
            