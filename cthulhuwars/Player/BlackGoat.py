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

    @property
    def dark_young_in_play(self):
        return self._dark_young_in_play

    @property
    def fungi_in_play(self):
        return self._fungi_in_play

    @property
    def ghouls_in_play(self):
        return self._ghouls_in_play

    def summon_dark_young(self, unit_zone):
        unit_cost = 3
        if self.spell_thousand_young:
            unit_cost = 2
        if self.power >= unit_cost:
            if self._dark_young_in_play < 3:
                new_dark_young = DarkYoung(self, unit_zone, unit_cost)
                self.add_unit(new_dark_young, unit_cost)
                self._dark_young_in_play += 1

    def summon_shub_niggurath(self, unit_zone):
        assert isinstance(unit_zone, Zone)
        print(text_colors.BOLD + 'The Black Goat is attempting to awaken Shub-Niggurath!' + text_colors.ENDC)
        unit_cost = 8
        if unit_zone.gate_state is GateState.occupied:
            if unit_zone.gate_unit.faction == self:
                if self.current_cultists >= 2:
                    shub_nigg = ShubNiggurath(self, unit_zone)
                    self.add_unit(shub_nigg,unit_cost)

                    for _ in range(2):
                        kill_list = []
                        for unit in self._units:
                            if unit.unit_type is UnitType.cultist and unit.unit_state is UnitState.in_play:
                                if unit.gate_state is not GateState.occupied:
                                    kill_list.append(unit)
                        print(self._color+'Pick a cultist to sacrifice:')
                        for n in range(kill_list.__len__()):
                            print('  ['+str(n)+'] Cultist in %s'%kill_list[n].unit_zone.name)
                        while True:
                            sacrifice = int(raw_input('Selection:'))
                            if sacrifice < kill_list.__len__():
                                break
                        self.remove_unit(kill_list[sacrifice])

                    print(text_colors.BOLD+'Shub-Niggurath Successfully Summoned!'+text_colors.ENDC)


    def spell_play_thousand_young(self):
        self.spell_thousand_young = True

    def spell_play_red_sign(self):
        self.spell_red_sign = True

    def spell_play_frenzy(self):
        self.spell_frenzy = True
        for unit in self._units:
            if unit.get_unit_type() is UnitType.cultist:
                unit.set_combat_power(1)

    def summon_action(self):
        if self.power >= 8:
            self.summon_shub_niggurath(self._home_zone)

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
class ShubNiggurath(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=8):
        super(ShubNiggurath, self).__init__(unit_parent, unit_zone, UnitType.GOO, combat_power=0, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)
    @property
    def combat_power(self):
        total_combat_power = self.faction.current_cultists + self.faction.current_gates
        if self.faction.spell_red_sign:
            total_combat_power += self.faction.dark_young_in_play
        return total_combat_power





