from time import sleep
from weakref import WeakKeyDictionary

from ClientChannel import ClientChannel
from Server import Server


class CWServer(Server):

    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        self.id = 0
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        self.nPlayers = 0
        self.maxPlayers = 4
        self.factions = {
            'cthulhu': False,
            'black_goat': False,
            'crawling_chaos': False,
            'yellow_sign': False
        }
        print 'Cthulhu Wars Server launched'

    def NextId(self):
        self.id += 1
        return self.id

    def Connected(self, channel, addr):
        self.AddPlayer(channel)

    def AddPlayer(self, player):
        if self.nPlayers < self.maxPlayers:
            self.nPlayers += 1
            print "New Player" + str(player.addr)
            self.players[player] = True
            player_faction = ''
            for k, v in self.factions.items():
                if v is False:
                    player_faction = k
                    self.factions[k] = True
                    break

            player.Send(
                {"action": "initial", "faction": player_faction})
            self.SendPlayers()
        else:
            print 'Maximum Players Reached'
            del player

    def DelPlayer(self, player):
        print "Deleting Player" + str(player.addr)
        del self.players[player]
        self.SendPlayers()

    def SendPlayers(self):
        self.SendToAll({"action": "players", "players": dict([(p.id, p.faction) for p in self.players])})

    def SendToAll(self, data):
        [p.Send(data) for p in self.players]

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)