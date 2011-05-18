import mplayer
import socket
import os

from Message import PlayerMessage, TamatarMessage

class Player():
    _id     = 0
    _client = None
    _libraryFile = '/home/root/audio/playlist.txt'
    _library = []
    _loop   = False
    _mode   = None
    _current = None
    MODE_FILE   = 1
    MODE_LIST   = 2
    
    def __init__(self, library=None, id=None):
        self._setupClient()
        if id is not None:
            self.setId(id)
        if library is not None:
            self._libraryFile = library
        self._loadLibrary()
        
        
    def setMode(self, mode):
        self._mode = mode
    def getMode(self):
        return self._mode
        
    def isPlaying(self):
        if not self.isAlive():
            return False
        fp = self._client.filepath
        if fp is not None:
            return True
        return False
    
    def filepath(self):
        if self.isAlive():
            return self._client.filepath

    def __del__(self):
        if (self._client is not None):
            pass
            #self._client.close()
    
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
        if snd == 'stop':
            self.stop()
        elif snd == 'all':
            self.playLibrary()
        else:
            self.play(snd)
        
    def parseRequest(self, payload, sender):
        # TamatarMessage
        msg = TamatarMessage()
        msg.fromString(payload)
        return msg
        
        
    def loop(self, val):
        self._loop = val
        
    def isLoop(self):
        return self._loop
            
    def checkLoop(self):
        if not self.isLoop():
            return
        if self.isPlaying():
            return
        if self._current is None:
            return
        mode = self.getMode()
        if mode == self.MODE_FILE:
            self.playFile(self._current)
        elif mode == self.MODE_LIST:
            self.playList(self._current)
        
    def playList(self, file, append=0):
        if self.isAlive():
            out = self._client.loadlist(file, append)
            self.setMode(self.MODE_LIST)
            self._current = file
        
    def playFile(self, file, append=0):
        if self.isAlive():
            out = self._client.loadfile(file, append)
            self.setMode(self.MODE_FILE)
            self._current = file
        
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
            self.setMode(None)
            self._current = None
        
            