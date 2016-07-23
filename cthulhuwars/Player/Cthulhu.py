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
        self._deep_one_in_play = 0
        self._shoggoth_in_play = 0
        self._starspawn_in_play = 0
        self._cthulhu_in_play = 0
        self._spell_dreams = False
        self._spell_yha_nthlei = False
        self._spell_devolve = False
        self._spell_regenerate = False
        self._spell_absorb = False
        self._spell_submerge = False
        self._color = text_colors.GREEN
        self.node_color = (0.2,0.8,0.2)

    def print_state(self):
        print (self._color)
        super(Cthulhu,self).print_state()


class DeepOne(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost):
        super(DeepOne, self).__init__(unit_parent, unit_zone, UnitType.monster, combat_power=0, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)
class Shoggoth(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost):
        super(Shoggoth, self).__init__(unit_parent, unit_zone, UnitType.monster, combat_power=2, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)

class Starspawn(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost):
        super(Starspawn, self).__init__(unit_parent, unit_zone, UnitType.monster, combat_power=3, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)
