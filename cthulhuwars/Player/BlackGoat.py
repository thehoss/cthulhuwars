from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState
from cthulhuwars.Maps import Map


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
        self._dark_young_in_play = 0
        self._fungi_in_play = 0
        self._ghouls_in_play = 0
        self._shub_nig_in_play = 0
        self.spell_thousand_young = False
        self.spell_frenzy = False
        self.spell_necrophagy = False
        self.spell_ghroth = False
        self.spell_red_sign = False
        self.spell_blood_sacrifice = False
        self._color = text_colors.RED

    def summon_dark_young(self, unit_zone):
        unit_cost = 3
        if self.spell_thousand_young:
            unit_cost = 2
        if self.power >= unit_cost:
            if self._dark_young_in_play < 3:
                new_dark_young = DarkYoung(self, unit_zone, unit_cost)
                self.add_unit(new_dark_young, unit_cost)
                self._dark_young_in_play += 1

    def spell_play_thousand_young(self):
        self.spell_thousand_young = True

    def spell_play_frenzy(self):
        self.spell_frenzy = True
        for unit in self._units:
            if unit.get_unit_type() is UnitType.cultist:
                unit.set_combat_power(1)

    def print_state(self):
        print (self._color)
        super(BlackGoat,self).print_state()


class Ghoul(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost):
        super(Ghoul, self).__init__(unit_parent, unit_zone, UnitType.monster, combat_power=0, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)
class Fungi(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost):
        super(Fungi, self).__init__(unit_parent, unit_zone, UnitType.monster, combat_power=1, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)

class DarkYoung(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost):
        super(DarkYoung, self).__init__(unit_parent, unit_zone, UnitType.monster, combat_power=2, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)


