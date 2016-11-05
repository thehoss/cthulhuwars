import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener
from thread import *
from cthulhuwars import Color, Board, Player

class CWClient(ConnectionListener):

    def __init__(self, host, port):
        self.Connect((host, port))
        self.players = {}
        self.statusLabel = 'connecting'
        self.playersLabel = "0 players"
        self.faction = ''
        self._player_class = None

    def sprint(self, msg, mode='info'):
        head = '[CWServer]: '
        if mode == 'info':
            print(Color.TextColor.GREEN+Color.TextColor.BOLD+head+msg)
        if mode == 'error':
            print(Color.TextColor.RED+Color.TextColor.BOLD+head+msg)
        if mode == 'warning':
            print(Color.TextColor.YELLOW+Color.TextColor.BOLD+head+msg)
        if mode == 'chat':
            print(Color.TextColor.BLUE+Color.TextColor.BOLD+msg)
        print(Color.TextColor.ENDC)

    def Loop(self):
        self.Pump()
        connection.Pump()

    def InputLoop(self):
        # horrid threaded input loop
        # continually reads from stdin and sends whatever is typed to the server
        # TODO: replace with command interpreter
        while 1:
            input = stdin.readline().rstrip("\n")
            if input == 'board':
                connection.Send({"action": "boardState"})
            elif input == 'me':
                connection.Send({"action": "me"})
            else:
                connection.Send({"action": "message", "message": input})

    def Network(self, data):
        #print 'network:', data
        pass

    def Network_connected(self, data):
        self.statusLabel = "connected"
        self.sprint("Connected to the server")

    def Network_error(self, data):
        self.sprint('error:'+data['error'][1], mode='error')
        import traceback
        traceback.print_exc()
        connection.Close()

    def Network_initial(self, data):
        self.faction = data['faction']
        self.sprint('joined as faction ' + self.faction)
        self.sprint('commands:  \n board = request board state from server \n me = print current player state')
        t = start_new_thread(self.InputLoop, ())
        #connection.Send({"action": "boardState"})

    def Network_disconnected(self, data):
        self.statusLabel += " - disconnected"
        self.sprint('Server disconnected', mode='warning')
        exit()

    def Network_players(self, data):
        self.sprint("*** players: " + ", ".join([p for p in data['players']]))

    def Network_message(self, data):
        self.sprint(data['who'] + ": " + data['message'], mode='chat')

    def Network_gameMessage(self, data):
        msg = data['message']
        print ''.join(msg)
