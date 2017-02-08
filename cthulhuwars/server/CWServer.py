import sys
sys.path.insert(0, '../../')
sys.path.insert(0, '.')
sys.path.insert(0, './PodSixNet')

from time import sleep
from weakref import WeakKeyDictionary

from ClientChannel import ClientChannel
from Server import Server
from cthulhuwars import Color, Board
from PrintStream import PrintStream

serveraddress=('localhost', int(666))

class CWServer(Server):
    '''
    ClientChannel class is used to communicate server data back to each client.  There is one ClientChannel per player
    '''
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        '''
        Init builds the board and map as well as the faction classes.  The factions are not set up until a player connects
        '''
        self.id = 0
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        self.nPlayers = 0
        self.maxPlayers = 4
        self.__player_turn = 0

        self.board = Board.Board()
        self.board.build_map()
        self.board.create_all_players()

        self.sprint('Cthulhu Wars Server launched')

    def NextId(self):
        self.id += 1
        return self.id

    def Connected(self, channel, addr):
        self.AddPlayer(channel)

    def sprint(self, msg, mode='info'):
        '''
        Custom print mechanism.  Just for pretty
        '''
        head = '[CWServer]: '
        if mode == 'info':
            print(Color.TextColor.GREEN+Color.TextColor.BOLD+head+msg)
        if mode == 'error':
            print(Color.TextColor.RED+Color.TextColor.BOLD+head+msg)
        if mode == 'warning':
            print(Color.TextColor.YELLOW+Color.TextColor.BOLD+head+msg)
        print(Color.TextColor.ENDC)

    def gameBegin(self):
        with PrintStream() as x:
            self.board.start()
        self.SendToAll({"action": "gameMessage", "message": x.data})

        i = 1
        num_rounds = 16
        r = 0
        winner = False
        with PrintStream() as x:
            self.board.gather_power_phase()
        self.SendToAll({"action": "gameMessage", "message": x.data})

        for _p in self.board.players:
            self.SendToAll({"action": "gameMessage", "message": "%s make your move!"%(_p.name)})
            for p in self.players:
                if p.faction == _p.short_name:
                    p.Send({"action": "gameTurn", "message": "Your Turn"})


    def AddPlayer(self, player):
        '''
        Adds a new player, selects a faction, sets up the faction object and places faction on the the board.
        This is called when a new client connects.
        :param player:
        :return: nothing
        '''
        if self.nPlayers < self.maxPlayers:
            self.nPlayers += 1
            self.sprint("New Player" + str(player.addr))
            self.players[player] = True
            available_factions = {}
            for k, v in self.board.player_dict.items():
                available_factions[k] = self.board.player_dict[k]['active']

            eastImage = self.board.map.eastMapImage
            westImage = self.board.map.westMapImage

            player.Send(
                {"action": "initial", "factions": available_factions, "mapImageData":[westImage, eastImage]}
            )
            if self.nPlayers == self.maxPlayers:
                self.gameBegin()
        else:
            self.sprint('Maximum Players Reached', mode='warning')
            del player

    def DelPlayer(self, player):
        '''
        Remove a player and it's client channel
        :param player:
        :return:
        '''
        self.sprint("Deleting Player" + str(player.addr), mode='warning')
        del self.players[player]
        self.nPlayers -= 1
        self.SendPlayers()

    def SendPlayers(self):
        '''
        This sends a list of current players to all players
        :return:
        '''
        self.SendToAll({"action": "players", "players": dict([(p.id, p.faction) for p in self.players])})

    def SendToAll(self, data):
        '''
        Sends data to all players
        :param data:
        :return:
        '''
        [p.Send(data) for p in self.players]

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)
if __name__ == "__main__":
    s = CWServer(localaddr=serveraddress)
    s.Launch()