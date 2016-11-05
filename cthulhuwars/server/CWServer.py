from time import sleep
from weakref import WeakKeyDictionary

from ClientChannel import ClientChannel
from Server import Server
from cthulhuwars import Color, Board

class CWServer(Server):

    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        self.id = 0
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        self.nPlayers = 0
        self.maxPlayers = 4

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
        head = '[CWServer]: '
        if mode == 'info':
            print(Color.TextColor.GREEN+Color.TextColor.BOLD+head+msg)
        if mode == 'error':
            print(Color.TextColor.RED+Color.TextColor.BOLD+head+msg)
        if mode == 'warning':
            print(Color.TextColor.YELLOW+Color.TextColor.BOLD+head+msg)
        print(Color.TextColor.ENDC)

    def AddPlayer(self, player):
        if self.nPlayers < self.maxPlayers:
            self.nPlayers += 1
            self.sprint("New Player" + str(player.addr))
            self.players[player] = True
            player_faction = ''
            for k, v in self.board.player_dict.items():
                if self.board.player_dict[k]['active'] is False:
                    player_faction = k
                    self.board.player_dict[k]['active'] = True
                    self.board.player_dict[k]['class'].player_setup()
                    player.player_class = self.board.player_dict[k]['class']
                    player.faction = player_faction
                    break
            self.sprint('assigning player %s to faction %s' % (str(player.addr), k))

            player.Send(
                {"action": "initial", "faction": player_faction }
            )
            self.SendPlayers()
        else:
            self.sprint('Maximum Players Reached', mode='warning')
            del player

    def DelPlayer(self, player):
        self.sprint("Deleting Player" + str(player.addr), mode='warning')
        del self.players[player]
        self.nPlayers -= 1
        self.SendPlayers()

    def SendPlayers(self):
        self.SendToAll({"action": "players", "players": dict([(p.id, p.faction) for p in self.players])})

    def SendToAll(self, data):
        [p.Send(data) for p in self.players]

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)