from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState

# Yellow Sign
# Starts in Europe
class text_colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class YellowSign(Player):
    def __init__(self, home_zone, name='The Yellow Sign'):
        super(YellowSign, self).__init__(Faction.yellow_sign, home_zone, name)
        self._color = text_colors.YELLOW

    def print_state(self):
        print (self._color)
        super(YellowSign,self).print_state()