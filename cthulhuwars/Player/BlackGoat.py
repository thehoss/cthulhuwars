from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState


# Black Goat
# Home Zone is Africa or East Africa:
# Zone('Africa', False)
class text_colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class BlackGoat(Player):
    def __init__(self, home_zone, name='The Black Goat'):
        super(BlackGoat, self).__init__(Faction.black_goat, home_zone, name)
        self.__dark_young_in_play = 0
        self.__fungi_in_play = 0
        self.__shub_nig_in_play = 0
        self.__ghouls_in_play = 0
        self.spell_thousand_young = False
        self.spell_frenzy = False
        self.spell_necrophagy = False
        self.spell_ghroth = False
        self.spell_red_sign = False
        self.spell_blood_sacrifice = False
        self.__color = text_colors.RED

    def summon_dark_young(self, unit_zone):
        unit_cost = 3
        if self.spell_thousand_young:
            unit_cost = 2
        if self.power >= unit_cost:
            if self.__dark_young_in_play < 3:
                new_dark_young = DarkYoung(self, unit_zone, unit_cost)
                self.add_unit(new_dark_young, unit_cost)
                self.__dark_young_in_play += 1

    def spell_play_thousand_young(self):
        self.spell_thousand_young = True

    def spell_play_frenzy(self):
        self.spell_frenzy = True
        for unit in self.__units:
            if unit.get_unit_type() is UnitType.cultist:
                unit.set_combat_power(1)

    def move_action(self):
        # we need to know who can move and to where
        # power determines how many moves we can make
        # after moving we also need to check for spell book
        # availability at 4 6 and 8 unique occupied zones
        occupied_zones = []
        candidate_moves = []
        power = self.power
        for unit in self.__units:
            occupied_zone.append(unit.unit_zone)
            # build list of possible moves to neighboring zones

        occupied_zones = list(set(occupied_zones))


    def print_state(self):
        print (self.__color)
        super(BlackGoat,self).print_state()

class DarkYoung(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost):
        super(DarkYoung, self).__init__(unit_parent, unit_zone, UnitType.monster, combat_power=2, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)
