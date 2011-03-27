#!/usr/bin/python
#
import socket
import os
import time
import re

HOST = '127.0.0.1'
PORT = 22044

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


# loop and process keyboard input
while True:
    s = raw_input('--> ')
    if (s != ''):
        print "sending %s\n" % s
        sock.send(s)
