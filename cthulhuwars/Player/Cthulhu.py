from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState

# The Great Cthulhu
# Starts in South Pacific
class text_colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Cthulhu(Player):
    def __init__(self, home_zone, name='Great Cthulhu'):
        super(Cthulhu, self).__init__(Faction.cthulhu, home_zone, name)
        self.__color = text_colors.GREEN

    def print_state(self):
        print (self.__color)
        super(Cthulhu,self).print_state()