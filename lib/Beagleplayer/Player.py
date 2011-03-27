import mplayer
import socket
import os

class Player():
    _client = None
    _libraryFile = '/home/root/audio/playlist.txt'
    _library = []

    def __init__(self, library=None):
        self._setupClient()
        if library is not None:
            self._libraryFile = library
        self._loadLibrary()

    def __del__(self):
        if (self._client is not None):
            self._client.close()

    def _loadLibrary(self):
        if os.path.isfile(self._libraryFile):
            try:
                fh = open(self._libraryFile, 'r')
                self._library = fh.readlines()
            except IOError as (errno, errmsg):
                print "failed opening library: '%s'" % (errmsg)
                return False
        return True
    
    def _setupClient(self):
        self._client = mplayer.Player()
        return True

    def request(self, msg, server):
        print "got request!"
        self.play(0)
        
    def playFile(self, file):
        if self._client is None or not self._client.is_alive():
            print "playFile: client not alive!"
            return False

        print "play file: %s " % (file)
        cmd = "loadfile %s" % (file)
        try:
            if not self._client.loadfile(file, 0):
                print "failed sending cmd '%s'" % (cmd)
                return False
        except socket.error, msg:
            print "failed sending cmd '%s'" % (msg)
            return False
        return True

    def play(self, index):
        f = int(index)
        if f >= 0 and f < len(self._library):
            return self.playFile(self._library[f])
        return False

    
