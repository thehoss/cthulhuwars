"""
 Crawling Chaos faction class
 Home Zone is Asia or South Asia:
 Zone('Asia', False)
"""

from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState
from cthulhuwars.Maps import Map
from cthulhuwars.DiceRoller import DiceRoller
from cthulhuwars.Color import TextColor, NodeColor

POOL = Zone('Pool')


class CrawlingChaos(Player):
    def __init__(self, home_zone, name='The Crawling Chaos'):
        super(CrawlingChaos, self).__init__(Faction.crawling_chaos, home_zone, name)
        '''
        Unit Lists
        The following lists are conveniences linking the relevant units from self._units
        '''
        self._nightgaunt = []
        self._flying_polyp = []
        self._hunting_horror = []
        self._nyarlathotep = None
        '''
        spell flags
        True = spell has been acquired by player
        '''
        self._spell_emissary_of_the_outer_gods = False
        self._spell_abduct = False
        self._spell_madness = False
        self._spell_the_thousand_forms = False
        self._spell_seek_and_destroy = False
        self._spell_invisibility = False
        '''
        drawing colors
        '''
        self._color = TextColor.BLUE
        self.node_color = NodeColor.BLUE

    @property
    def nightgaunt_in_play(self):
        result = 0
        for ng in self._nightgaunt:
            if ng.unit_state is UnitState.in_play:
                result += 1
        return result

    @property
    def flying_polyp_in_play(self):
        result = 0
        for fp in self._flying_polyp:
            if fp.unit_state is UnitState.in_play:
                result += 1
        return result

    @property
    def hunting_horror_in_play(self):
        result = 0
        for hh in self._hunting_horror:
            if hh.unit_state is UnitState.in_play:
                result += 1
        return result

    @property
    def goo_in_play(self):
        return self._nyarlathotep.__len__()

    def player_setup(self):
        super(CrawlingChaos, self).player_setup()
        n_nightgaunt = 3
        n_flying_polyp = 3
        n_hunting_horror = 2
        for _ in range(n_nightgaunt):
            new_ng = Nightgaunt(self, POOL)
            self.add_unit(new_ng)
            self._nightgaunt.append(new_ng)

        for _ in range(n_flying_polyp):
            new_fp = FlyingPolyp(self, POOL)
            self.add_unit(new_fp)
            self._flying_polyp.append(new_fp)

        for _ in range(n_hunting_horror):
            new_hh = HuntingHorror(self, POOL)
            self.add_unit(new_hh)
            self._hunting_horror.append(new_hh)

        self._nyarlathotep = Nyarlathotep(self, POOL)
        self.add_unit(self._nyarlathotep)

    def summon_nightgaunt(self, unit_zone):
        unit_cost = 1
        if self.power >= unit_cost:
            for nightgaunt in self._nightgaunt:
                if nightgaunt.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + TextColor.BOLD + 'A Nightgaunt descends from above!' + TextColor.ENDC)
                        nightgaunt.set_unit_state(UnitState.in_play)
                        nightgaunt.set_unit_zone(unit_zone)
                        return True
        return False

    def summon_flying_polyp(self, unit_zone):
        unit_cost = 2
        if self.power >= unit_cost:
            for flying_polyp in self._flying_polyp:
                if flying_polyp.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + TextColor.BOLD + 'A Flying Polyp appears!' + TextColor.ENDC)
                        flying_polyp.set_unit_state(UnitState.in_play)
                        flying_polyp.set_unit_zone(unit_zone)
                        return True
        return False


class Nightgaunt(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(Nightgaunt, self).__init__(unit_parent, unit_zone, UnitType.monster, combat_power=0, cost=unit_cost,
                                         base_movement=2,
                                         unit_state=UnitState.in_reserve)


class FlyingPolyp(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(FlyingPolyp, self).__init__(unit_parent, unit_zone, UnitType.monster, combat_power=1, cost=unit_cost,
                                          base_movement=2,
                                          unit_state=UnitState.in_reserve)


class HuntingHorror(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(HuntingHorror, self).__init__(unit_parent, unit_zone, UnitType.monster, combat_power=2, cost=unit_cost,
                                            base_movement=2,
                                            unit_state=UnitState.in_reserve)


class Nyarlathotep(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=10):
        super(Nyarlathotep, self).__init__(unit_parent, unit_zone, UnitType.GOO, combat_power=0, cost=unit_cost,
                                           base_movement=2,
                                           unit_state=UnitState.in_reserve)