from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState

class BlackGoat(Player):
    def __init__(self, faction=Faction.black_goat, home_zone=Zone('Africa', False), name='The  Black Goat'):
        super(BlackGoat, self).__init__(faction, home_zone, name)
