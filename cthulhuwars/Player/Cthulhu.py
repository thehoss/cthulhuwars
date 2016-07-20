from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState

class Cthulhu(Player):
    def __init__(self, faction=Faction.cthulhu, home_zone=Zone('South Pacific', False), name='Great Cthulhu'):
        super(Cthulhu, self).__init__(faction, home_zone, name)
