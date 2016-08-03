"""
 The Great Cthulhu
 Starts in South Pacific
"""

from core import Player
from cthulhuwars.Color import TextColor, NodeColor
from cthulhuwars.DiceRoller import DiceRoller
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState
from cthulhuwars.Maps import Map

class Cthulhu(Player):
    def __init__(self, home_zone, board, name='Great Cthulhu'):
        super(Cthulhu, self).__init__(Faction.cthulhu, home_zone, board, name)
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
        self._color = TextColor.GREEN
        self._node_color = NodeColor.GREEN

    def player_setup(self):
        super(Cthulhu, self).player_setup()
        n_deep_ones = 4
        n_shoggoth = 2
        n_starspawn = 2
        for _ in range(n_deep_ones):
            new_do = DeepOne(self, self._pool)
            self.add_unit(new_do)
            self._deep_ones.append(new_do)
            self._monsters.append(new_do)

        for _ in range(n_shoggoth):
            new_s = Shoggoth(self, self._pool)
            self.add_unit(new_s)
            self._shoggoth.append(new_s)
            self._monsters.append(new_s)

        for _ in range(n_starspawn):
            new_ss = Starspawn(self, self._pool)
            self.add_unit(new_ss)
            self._starspawn.append(new_ss)
            self._monsters.append(new_ss)

        self._cthulhu = GreatCthulhu(self, self._pool)
        self.add_unit(self._cthulhu)
        self._goo.append(self._cthulhu)
        self._monsters.append(self._cthulhu)

    def summon_deep_one(self, unit_zone):
        unit_cost = 1
        if self.power >= unit_cost:
            for deep_one in self._deep_ones:
                if deep_one.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + TextColor.BOLD + 'A Deep One has surfaced!' + TextColor.ENDC)
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
                        print(self._color + TextColor.BOLD + 'A Shoggoth oozes forth!' + TextColor.ENDC)
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
                        print(self._color + TextColor.BOLD + 'A Starspawn reveals itself!' + TextColor.ENDC)
                        ss.set_unit_state(UnitState.in_play)
                        ss.set_unit_zone(unit_zone)
                        return True
        return False

    def summon_cthulhu(self, unit_zone):
        unit_cost = 10
        if self._immortal:
            unit_cost = 4
        if self._home_zone.gate_state is not GateState.noGate:
            if self.power >= unit_cost:
                cthulhu = self._cthulhu
                if cthulhu.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + TextColor.BOLD + 'The Great Cthulhu has emerged!' + TextColor.ENDC)
                        cthulhu.set_unit_state(UnitState.in_play)
                        cthulhu.set_unit_zone(self._home_zone)
                        self._immortal = True
                        self._elder_points += DiceRoller(1, 3).roll_dice()[0]
                        return True
        return False

    def summon_action(self, monster, unit_zone):
        assert isinstance(monster, Unit)
        if monster.unit_state is UnitState.in_reserve:
            if monster.unit_type is UnitType.cthulhu:
                return self.summon_cthulhu(unit_zone)
            if monster.unit_type is UnitType.deep_one:
                return self.summon_deep_one(unit_zone)
            if monster.unit_type is UnitType.shoggoth:
                return self.summon_shoggoth(unit_zone)
            if monster.unit_type is UnitType.star_spawn:
                return self.summon_starspawn(unit_zone)
        return False

    '''
    find_move_actions
    returns a list of all possible move actions based on current state of units on the board
    This method scores each move according to desirability in the field
    this list is a tuple: (the unit that can move, the zone in which the unit currently resides, the destination zone, score)
    '''
    def find_move_actions(self, map):
        assert isinstance(map, Map)
        # we need to know who can move and to where
        # power determines how many moves we can make
        # after moving we also need to check for spell book
        # availability
        all_possible_moves = []
        for unit in self._units:
            if self.power >= 1:
                if unit.unit_state is UnitState.in_play and unit.gate_state is not GateState.occupied:
                    score = 0
                    assert isinstance(unit, Unit)

                    # build list of possible moves to neighboring zones
                    neighbors = map.find_neighbors(unit.unit_zone.name, unit.base_movement)
                    for n in neighbors:
                        destination_zone = map.zone_by_name(n)
                        assert isinstance(destination_zone, Zone)
                        if destination_zone.gate_state is GateState.emptyGate:
                            score += 2
                        if destination_zone.is_ocean is True:
                            score += 1
                        for occupant in destination_zone.occupancy_list:
                            assert isinstance(occupant, Unit)
                            if occupant.unit_type is UnitType.cultist and unit.unit_type is not UnitType.cultist:
                                score += 1
                            if occupant.unit_type is not UnitType.cultist:
                                score -= 1
                        if len(destination_zone.occupancy_list) == 0:
                            score += 1

                        all_possible_moves.append((unit, unit.unit_zone, destination_zone, score))

                elif unit.gate_state is GateState.occupied:
                    print(self._color + '%s %s in %s is maintaining a gate' % (
                        self._faction.value, unit.unit_type.value, unit.unit_zone.name) + TextColor.ENDC)
        return all_possible_moves

class DeepOne(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(DeepOne, self).__init__(unit_parent, unit_zone, UnitType.deep_one, combat_power=1, cost=unit_cost,
                                      base_movement=1,
                                      unit_state=UnitState.in_reserve)

    def render_unit(self):
        render_definition = {
            "nodetype": ["sphere"],
            "name": ["%s_%s" % (self.faction._name, self._unit_type.value)],
            "params": [("float", "radius", 0.025)]
        }
        return render_definition


class Shoggoth(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(Shoggoth, self).__init__(unit_parent, unit_zone, UnitType.shoggoth, combat_power=2, cost=unit_cost,
                                       base_movement=1,
                                       unit_state=UnitState.in_reserve)

    def render_unit(self):
        render_definition = {
            "nodetype": ["sphere"],
            "name": ["%s_%s" % (self.faction._name, self._unit_type.value)],
            "params": [("float", "radius", 0.030)]
        }
        return render_definition


class Starspawn(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(Starspawn, self).__init__(unit_parent, unit_zone, UnitType.star_spawn, combat_power=3, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)

    def render_unit(self):
        render_definition = {
            "nodetype": ["sphere"],
            "name": ["%s_%s" % (self.faction._name, self._unit_type.value)],
            "params": [("float", "radius", 0.03)]
        }
        return render_definition


class GreatCthulhu(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(GreatCthulhu, self).__init__(unit_parent, unit_zone, UnitType.cthulhu, combat_power=6, cost=unit_cost,
                                           base_movement=1,
                                           unit_state=UnitState.in_reserve)

    def render_unit(self):
        render_definition = {
            "nodetype": ["procedural"],
            "name": ["cthulhu_object"],
            "params": [("string", "dso", "c:/Users/Adam Martinez/PycharmProjects/cthulhuwars/obj/cthulhu_goo.obj"),
                       ("bool", "load_at_init", 1)]
        }
        return render_definition
