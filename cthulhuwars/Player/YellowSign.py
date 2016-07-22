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
        self._undead_in_play = 0
        self._byakhee_in_play = 0
        self._king_in_yellow_in_play = 0
        self._hastur_in_play = 0
        self._color = text_colors.YELLOW

    def print_state(self):
        print (self._color)
        super(YellowSign,self).print_state()

class Undead(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost):
        super(Undead, self).__init__(unit_parent, unit_zone, UnitType.monster, combat_power=None, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)
class Byakhee(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost):
        super(Byakhee, self).__init__(unit_parent, unit_zone, UnitType.monster, combat_power=None, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)
