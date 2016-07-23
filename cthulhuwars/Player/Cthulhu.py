from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState
from cthulhuwars.DiceRoller import DiceRoller

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

NULL_ZONE = Zone('null zone')

class Cthulhu(Player):
    def __init__(self, home_zone, name='Great Cthulhu'):
        super(Cthulhu, self).__init__(Faction.cthulhu, home_zone, name)
        self._deep_ones = []
        self._shoggoth = []
        self._starspawn = []
        self._cthulhu = []
        self._immortal = False
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

    def player_setup(self):
        super(Cthulhu, self).player_setup()
        n_deep_ones = 4
        n_shoggoth = 2
        n_starspawn = 2
        for _ in range(n_deep_ones):
            new_do = DeepOne(self, NULL_ZONE)
            self.add_unit(new_do)
            self._deep_ones.append(new_do)

        for _ in range(n_shoggoth):
            new_s = Shoggoth(self, NULL_ZONE)
            self.add_unit(new_s)
            self._shoggoth.append(new_s)

        for _ in range(n_starspawn):
            new_s = Starspawn(self, NULL_ZONE)
            self.add_unit(new_s)
            self._starspawn.append(new_s)

        self._cthulhu= GreatCthulhu(self, NULL_ZONE)
        self.add_unit(self._cthulhu)

    def summon_deep_one(self, unit_zone):
        unit_cost = 1
        if self.power >= unit_cost:
            for deep_one in self._deep_ones:
                if deep_one.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + text_colors.BOLD + 'A Deep One has surfaced!' + text_colors.ENDC)
                        deep_one.set_unit_state(UnitState.in_play)
                        deep_one.set_unit_zone(unit_zone)
                        return True
        return False

    def summon_shoggoth(self, unit_zone):
        unit_cost = 1
        if self.power >= unit_cost:
            for shog in self._shoggoth:
                if shog.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + text_colors.BOLD + 'A Shoggoth oozes forth!' + text_colors.ENDC)
                        shog.set_unit_state(UnitState.in_play)
                        shog.set_unit_zone(unit_zone)
                        return True
        return False

    def summon_starspawn(self, unit_zone):
        unit_cost = 1
        if self.power >= unit_cost:
            for ss in self._starspawn:
                if ss.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + text_colors.BOLD + 'A Starspawn reveals itself!' + text_colors.ENDC)
                        ss.set_unit_state(UnitState.in_play)
                        ss.set_unit_zone(unit_zone)
                        return True
        return False

    def summon_cthulhu(self, unit_zone):
        unit_cost = 10
        if self._immortal:
            unit_cost = 4
        if self.power >= unit_cost:
            for cthulhu in self._cthulhu:
                if cthulhu.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + text_colors.BOLD + 'The Great Cthulhu has emerged!' + text_colors.ENDC)
                        cthulhu.set_unit_state(UnitState.in_play)
                        cthulhu.set_unit_zone(unit_zone)
                        self._immortal = True
                        self._elder_points += DiceRoller(1,3).roll_dice()[0]
                        return True
        return False

    def summon_action(self):
        unit_zone = None

        summon = [self.summon_cultist,
                  self.summon_deep_one,
                  self.summon_cthulhu,
                  self.summon_shoggoth,
                  self.summon_starspawn
                  ]

        for cultist in self._cultists:
            if cultist.gate_state is GateState.occupied:
                unit_zone = cultist.unit_zone

        if unit_zone is not None:
            '''RANDOM_PLAYOUT'''
            dice = DiceRoller(1, 5)
            dice_result = dice.roll_dice()[0]-1
            summon[dice_result](unit_zone)


class DeepOne(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(DeepOne, self).__init__(unit_parent, unit_zone, UnitType.deep_one, combat_power=1, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)
class Shoggoth(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(Shoggoth, self).__init__(unit_parent, unit_zone, UnitType.shoggoth, combat_power=2, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)

class Starspawn(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(Starspawn, self).__init__(unit_parent, unit_zone, UnitType.star_spawn, combat_power=3, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)

class GreatCthulhu(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(GreatCthulhu, self).__init__(unit_parent, unit_zone, UnitType.cthulhu, combat_power=6, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)
