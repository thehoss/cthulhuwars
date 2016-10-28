import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener
from thread import *
class CWClient(ConnectionListener):

    def __init__(self, host, port):
        self.Connect((host, port))
        self.players = {}
        self.statusLabel = 'connecting'
        self.playersLabel = "0 players"
        self.faction = ''

    def Loop(self):
        self.Pump()
        connection.Pump()

    def InputLoop(self):
        # horrid threaded input loop
        # continually reads from stdin and sends whatever is typed to the server
        while 1:
            connection.Send({"action": "message", "message": stdin.readline().rstrip("\n")})

    def Network(self, data):
        #print 'network:', data
        pass


    def Network_connected(self, data):
        self.statusLabel = "connected"
        print "Connected to the server"

    def Network_error(self, data):
        print 'error:', data['error'][1]
        import traceback
        traceback.print_exc()
        connection.Close()

    def Network_initial(self, data):
        self.faction = data['faction']
        t = start_new_thread(self.InputLoop, ())
        connection.Send({"action": "initial", "faction": self.faction})
        print 'joined as faction '+ self.faction

    def Network_disconnected(self, data):
        self.statusLabel += " - disconnected"
        print 'Server disconnected'
        exit()

    def Network_players(self, data):
        print "*** players: " + ", ".join([p for p in data['players']])

    def Network_message(self, data):
        print data['who'] + ": " + data['message']