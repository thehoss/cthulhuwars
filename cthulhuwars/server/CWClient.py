from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener
from thread import *
from cthulhuwars import Color
from Board import Factions

serveraddress=('localhost', int(666))

class CWClient(ConnectionListener):

    def __init__(self, host='localhost', port=int(666)):
        '''
        A thin client.  This class is the user interface to the game.  Game and player state are kept only on the server
        Client requests data and posts commands.
        :param host:
        :param port:
        '''
        self.players = {}
        self.statusLabel = 'connecting'
        self.playersLabel = "0 players"
        self.faction = ''
        self.Connect((host, port))

    def sprint(self, msg, mode='info'):
        '''
        for to make pretty printing
        :param msg:
        :param mode:
        :return:
        '''
        head = '[CWClient]: '
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

    def Launch(self):
        while True:
            self.Loop()
            sleep(0.001)

    def InputLoop(self):
        '''
        horrid threaded input loop
        continually reads from stdin and sends whatever is typed to the server
        TODO: replace with command interpreter
        '''
        while 1:
            input = stdin.readline().rstrip("\n")
            if input == 'board':
                connection.Send({"action": "boardState"})
            elif input == 'me':
                connection.Send({"action": "me"})
            elif input == 'dc':
                connection.Send({"action": "disconnect"})
            else:
                connection.Send({"action": "message", "message": input})

    def Network(self, data):
        # print 'network:', data
        pass

    def Network_connected(self, data):
        '''
        called when connected action is sent
        :param data:
        :return:
        '''
        self.statusLabel = "connected"
        self.sprint("Connected to the server")

    def Network_error(self, data):
        '''
        report errors from the server
        :param data:
        :return:
        '''
        self.sprint('error:'+data['error'], mode='error')
        import traceback
        traceback.print_exc()
        connection.Close()
        exit(-1)

    def Network_initial(self, data):
        '''
        called when initial action is sent by server, after client connect
        :param data:
        :return:
        '''
        available_factions = data['factions']
        valid = False
        validVals = []
        while valid is False:
            print ('Select your Great Old One:')
            if available_factions['cthulhu'] is False:
                print(Color.TextColor.GREEN + ' [1] The Great Cthulhu' + Color.TextColor.ENDC)
                validVals.append(1)
            if available_factions['black_goat'] is False:
                print(Color.TextColor.RED + ' [2] The Black Goat' + Color.TextColor.ENDC)
                validVals.append(2)
            if available_factions['crawling_chaos'] is False:
                print(Color.TextColor.BLUE + ' [3] The Crawling Chaos' + Color.TextColor.ENDC)
                validVals.append(3)
            if available_factions['yellow_sign'] is False:
                print(Color.TextColor.YELLOW + ' [4] The Yellow Sign' + Color.TextColor.ENDC)
                validVals.append(4)
            selection = int(raw_input("Selection: "))

            if selection in validVals:
                valid = True

        self.faction = Factions[selection-1]

        self.sprint('joined as faction ' + self.faction)
        self.sprint('commands:  \n board = request board state from server \n me = print current player state')
        connection.Send({"action": "faction", "faction": self.faction})

        t = start_new_thread(self.InputLoop, ())
        #connection.Send({"action": "boardState"})

    def Network_disconnected(self, data):
        self.statusLabel += " - disconnected"
        self.sprint('Server disconnected * ', mode='warning')
        exit()

    def Network_players(self, data):
        '''
        prints the player data from the server
        :param data:
        :return:
        '''
        self.sprint("*** players: " + ", ".join([p for p in data['players']]))

    def Network_message(self, data):
        '''
        prints a message from another client
        :param data:
        :return:
        '''
        self.sprint(data['who'] + ": " + data['message'], mode='chat')

    def Network_gameMessage(self, data):
        '''
        prints a game message from the server
        :param data:
        :return:
        '''
        msg = data['message']
        print ''.join(msg)

if __name__ == "__main__":
    c = CWClient(host=serveraddress[0], port=serveraddress[1])
    c.Launch()