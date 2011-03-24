import mplayer
import socket
import os

class Player():
    _client = None
    _libraryFile = '/home/root/audio/playlist.txt'
    _library = []

    def __init__(self):
        self._setupClient()
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
        self._client = mplayer.Client()
        try:
            print "connecting to MPlayer on localhost:1025"
            self._client.connect(('localhost', 1025))
        except:
            print "connection to MPlayer failed"
            self._client.close()
            return False

        try:
            self._client.send("")
        except socket.error, msg:
            print "failed initializing MPlayer"
            print msg
            return False

        return True


    def playFile(self, file):
        if self._client is None or not self._client.connected:
            print "playFile: client not connected!"
            return False

        cmd = "loadfile %s" % (file)
        try:
            if not self._client.send_command(cmd):
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

    
