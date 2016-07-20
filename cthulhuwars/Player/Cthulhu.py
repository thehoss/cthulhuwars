from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState

# The Great Cthulhu
# Starts in South Pacific

class Cthulhu(Player):
    def __init__(self, home_zone, name='Great Cthulhu'):
        super(Cthulhu, self).__init__(Faction.cthulhu, home_zone, name)
