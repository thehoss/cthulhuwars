"""
 Crawling Chaos faction class
 Home Zone is Asia or South Asia:
 Zone('Asia', False)
"""

import random
from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState
from cthulhuwars.Maps import Map
from cthulhuwars.DiceRoller import DiceRoller
from cthulhuwars.Color import TextColor, NodeColor

class CrawlingChaos(Player):
    def __init__(self, home_zone, board, name='The Crawling Chaos'):
        super(CrawlingChaos, self).__init__(Faction.crawling_chaos, home_zone, board, name)
        '''
        Unit Lists
        The following lists are conveniences linking the relevant units from self._units
        '''
        self._nightgaunt = set()
        self._flying_polyp = set()
        self._hunting_horror = set()
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
        self._node_color = NodeColor.BLUE
        self.awakened_nyarlathotep = False

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
            new_ng = Nightgaunt(self, self._pool)
            self.add_unit(new_ng)
            self._nightgaunt.add(new_ng)
            self._monsters.add(new_ng)

        for _ in range(n_flying_polyp):
            new_fp = FlyingPolyp(self, self._pool)
            self.add_unit(new_fp)
            self._flying_polyp.add(new_fp)
            self._monsters.add(new_fp)

        for _ in range(n_hunting_horror):
            new_hh = HuntingHorror(self, self._pool)
            self.add_unit(new_hh)
            self._hunting_horror.add(new_hh)
            self._monsters.add(new_hh)

        self._nyarlathotep = Nyarlathotep(self, self._pool)
        self.add_unit(self._nyarlathotep)
        self._goo.add(self._nyarlathotep)

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

    def summon_hunting_horror(self, unit_zone):
        unit_cost = 3
        if self.power >= unit_cost:
            for hh in self._hunting_horror:
                if hh.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + TextColor.BOLD + 'A Hunting Horror descends from above!' + TextColor.ENDC)
                        hh.set_unit_state(UnitState.in_play)
                        hh.set_unit_zone(unit_zone)
                        return True
        return False

    def summon_nyarlathotep(self, unit_zone):
        assert isinstance(unit_zone, Zone)
        print(
            self._color + TextColor.BOLD + 'The Crawling Chaos is attempting to awaken Nyarlathotep!' + TextColor.ENDC)
        unit_cost = 10
        # Do we have enough power?
        if self.power >= unit_cost:
            # is there a gate in the summoning zone, and do we occupy it?
            if unit_zone.gate_state is GateState.occupied:
                if unit_zone.gate_unit.faction == self:

                    # put Nyarlathotep on the board, and spend the power
                    self._nyarlathotep.set_unit_zone(unit_zone)
                    self._nyarlathotep.set_unit_state(UnitState.in_play)
                    self.spend_power(unit_cost)
                    if not self.awakened_nyarlathotep:
                        self.awakened_nyarlathotep = True
                        self.take_new_spell()
                    print(self._color + TextColor.BOLD + 'Nyarlathotep Successfully Summoned!' + TextColor.ENDC)
                    return True
        return False


    def spell_emissary_of_the_outer_gods(self):
        self._spell_emissary_of_the_outer_gods = True


    def spell_abduct(self):
        self.spell_abduct = True


    def spell_madness(self):
        self.spell_madness = True


    def spell_the_thousand_forms(self):
        self.spell_the_thousand_forms = True


    def spell_seek_and_destroy(self):
        self.spell_seek_and_destroy = True


    def spell_invisibility(self):
        self._spell_invisibility = True


    def take_new_spell(self):
        # check conditions for taking a new spell:

        # As action for a round, pay 4 power
        if not self._spell_requirement_met[0] and self._power_spent == 4:
            self._spell_requirement_met[0] = True

        # As action for a round, pay 6 power
        if not self._spell_requirement_met[1] and self._power_spent == 6:
            self._spell_requirement_met[1] = True

        # Control 3 gates or have 12 power
        if not self._spell_requirement_met[2] and self.current_gates == 3 or self._power == 12:
            self._spell_requirement_met[2] = True

        # Control 4 gates or have 15 power
        if not self._spell_requirement_met[3] and self.current_gates == 4 or self._power == 15:
            self._spell_requirement_met[3] = True

        # Capture an enemy Cultist
        if not self._spell_requirement_met[4] and self._captured_cultists.__len__() > 0:
            self._spell_requirement_met[4] = True

        # Awaken Nyarlathotep
        if not self._spell_requirement_met[5] and self._goo.__len__() > 0:
            self._spell_requirement_met[5] = True

    def summon_action(self, monster, unit_zone):
        assert isinstance(monster, Unit)
        if monster.unit_state is UnitState.in_reserve:
            if monster.unit_type is UnitType.flying_polyp:
                return self.summon_flying_polyp(unit_zone)
            if monster.unit_type is UnitType.hunting_horror:
                return self.summon_hunting_horror(unit_zone)
            if monster.unit_type is UnitType.nightgaunt:
                return self.summon_nightgaunt(unit_zone)
            if monster.unit_type is UnitType.nyarlathotep:
                return self.summon_nyarlathotep(unit_zone)
        return False


    def recompute_power(self):
        super(CrawlingChaos, self).recompute_power()


class Nightgaunt(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(Nightgaunt, self).__init__(unit_parent, unit_zone, UnitType.nightgaunt, combat_power=0, cost=unit_cost,
                                         base_movement=2,
                                         unit_state=UnitState.in_reserve)

    def render_unit(self):
        render_definition = {
            "nodetype": ["sphere"],
            "name": ["%s_%s" % (self.faction._name, self._unit_type.value)],
            "params": [("float", "radius", 0.035)]
        }
        return render_definition

class FlyingPolyp(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(FlyingPolyp, self).__init__(unit_parent, unit_zone, UnitType.flying_polyp, combat_power=1, cost=unit_cost,
                                          base_movement=2,
                                          unit_state=UnitState.in_reserve)

    def render_unit(self):
        render_definition = {
            "nodetype": ["sphere"],
            "name": ["%s_%s" % (self.faction._name, self._unit_type.value)],
            "params": [("float", "radius", 0.035)]
        }
        return render_definition

class HuntingHorror(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(HuntingHorror, self).__init__(unit_parent, unit_zone, UnitType.hunting_horror, combat_power=2, cost=unit_cost,
                                            base_movement=2,
                                            unit_state=UnitState.in_reserve)


    def render_unit(self):
        render_definition = {
            "nodetype": ["sphere"],
            "name": ["%s_%s" % (self.faction._name, self._unit_type.value)],
            "params": [("float", "radius", 0.035)]
        }
        return render_definition

class Nyarlathotep(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=10):
        super(Nyarlathotep, self).__init__(unit_parent, unit_zone, UnitType.nyarlathotep, combat_power=0, cost=unit_cost,
                                           base_movement=2,
                                           unit_state=UnitState.in_reserve)
    def render_unit(self):
        render_definition = {
            "nodetype": ["sphere"],
            "name": ["%s_%s" % (self.faction._name, self._unit_type.value)],
            "params": [("float", "radius", 0.08)]
        }
        return render_definition