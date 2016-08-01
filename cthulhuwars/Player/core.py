from enum import Enum
import random
from functools import partial
from numpy.random import choice
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction, Cultist
from cthulhuwars.Zone import Zone, GateState
from cthulhuwars.Maps import Map
from cthulhuwars.Color import TextColor
from cthulhuwars.Color import NodeColor


# Generic Player class
# Overridden by faction specific subclasses
# home_zone left intentionally without default since the Board needs to pass in the
# Zone class instance from the map construction

class possible_actions(Enum):
    move = 0
    summon = 1
    build = 2
    capture = 3
    recruit = 4
    awaken = 5
    combat = 6
    passturn = 7


POOL = Zone('Pool')


class Player(object):
    def __init__(self, faction, home_zone, board, name='Player1'):
        assert isinstance(home_zone, Zone)
        self._name = name
        self._faction = faction
        self._home_zone = home_zone
        self._spells = [6]
        self._spell_requirements_met = [False] * 6
        self._units = []
        self._cultists = []
        self._monsters = []
        self._goo = []
        self._power = 8
        self._power_spent = 0
        self._doom_points = 0
        self._elder_points = 0
        self._starting_cultists = 6
        self._current_cultists = 0
        self._captured_cultists = []
        self._current_gates = 0
        self._occupied_zones = []
        self._color = TextColor.GREEN
        self._node_color = NodeColor.GREEN
        self._board = board
        self._pool = POOL
        self.probability_dict = {
            'capture': 0.3,
            'build': 0.25,
            'move': 0.25,
            'summon': 0.1,
            'recruit': 0.1,
            'combat': 0,
            'awaken': 0,
            'special': 0
        }

    def player_setup(self):
        # add starting gate and cultist to home zone
        # add remaining cultists
        movement_max_radius = 1
        if self._faction == Faction.crawling_chaos:
            movement_max_radius = 2
        for _ in range(self._starting_cultists):
            new_cultist = Cultist(self, self._home_zone, movement_max_radius, UnitState.in_play)
            self.add_unit(new_cultist)
            self._cultists.append(new_cultist)
        self.build_gate_action(self._cultists[0], self._home_zone)

    def recruit_cultist(self, unit_zone):
        unit_cost = 1
        if self.power >= unit_cost:
            for cultist in self._cultists:
                if cultist.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        cultist.set_unit_state(UnitState.in_play)
                        cultist.set_unit_zone(unit_zone)
                        return True
        return False

    def kill_unit(self, unit):
        assert isinstance(unit, Unit)
        unit.set_unit_state(UnitState.killed)
        unit.set_unit_zone(self._pool)
        return True

    def remove_unit(self, unit):
        assert isinstance(unit, Unit)
        unit.set_unit_state(UnitState.in_reserve)
        unit.set_unit_zone(self._pool)
        return True

    def capture_unit(self, monster, unit_zone, unit):
        assert isinstance(unit, Unit)
        assert isinstance(monster, Unit)
        assert isinstance(unit_zone, Zone)

        if unit.unit_type is UnitType.cultist:
            if self.spend_power(1):
                print(self._color  + TextColor.BOLD + "%s %s has captured %s %s in %s" % (
                    self._name, monster.unit_type.value, unit.faction._name, unit.unit_type.value,
                    unit.unit_zone.name) + TextColor.ENDC)
                if unit.gate_state is GateState.occupied:
                    unit.set_unit_gate_state(GateState.noGate)
                    unit_zone.clear_gate_state()
                    self.capture_gate(monster)
                self._captured_cultists.append(unit)
                unit.set_unit_state(UnitState.captured)
                unit.set_unit_zone(self._pool)
                return True
        return False

    def occupied_zones(self):
        self._occupied_zones = []
        for unit in self._units:
            if unit.unit_state is UnitState.in_play:
                self._occupied_zones.append(unit.unit_zone)
        self._occupied_zones = list(set(self._occupied_zones))
        return self._occupied_zones.__len__()

    @property
    def power(self):
        return self._power

    @property
    def faction(self):
        return self._faction

    @property
    def current_cultists(self):
        cultists = 0
        for c in self._cultists:
            assert isinstance(c, Cultist)
            if c.unit_zone is not self._pool and c.unit_state is UnitState.in_play:
                cultists += 1
        self._current_cultists = cultists
        return self._current_cultists

    @property
    def cultists_in_play(self):
        cultists = 0
        cultists_in_play = []
        for c in self._cultists:
            assert isinstance(c, Cultist)
            if c.unit_zone is not self._pool and c.unit_state is UnitState.in_play:
                cultists += 1
                cultists_in_play.append(c)
        self._current_cultists = cultists
        return cultists_in_play

    @property
    def captured_cultists(self):
        return self._captured_cultists.__len__()

    @property
    def current_gates(self):
        gates = 0
        for cultist in self._cultists:
            if cultist.gate_state is GateState.occupied and cultist.unit_zone is not self._pool:
                gates += 1
        self._current_gates = gates
        return self._current_gates

    def abandon_gate(self, unit):
        assert isinstance(unit, Cultist)
        if unit.gate_state is GateState.occupied:
            unit.set_unit_gate_state(GateState.noGate)
            unit.unit_zone.clear_gate_state()
            self._current_gates -= 1
            return True
        return False

    def capture_gate(self, unit):
        if unit.unit_type is UnitType.cultist:
            assert isinstance(unit, Cultist)
            if unit.gate_state is not GateState.occupied:
                if unit.unit_zone.gate_state is GateState.emptyGate:
                    unit.set_unit_gate_state(GateState.occupied)
                    unit.unit_zone.set_gate_unit(unit)
                    self._current_gates += 1
                    print(self._color + "%s %s has taken control of a gate in %s" % (
                        unit.faction._name, unit.unit_type.value, unit.unit_zone.name) + TextColor.ENDC)
                    return True
        return False

    def add_unit(self, new_unit):
        self._units.append(new_unit)
        if new_unit.unit_type is not UnitType.cultist:
            self._monsters.append(new_unit)
        if new_unit.unit_type is UnitType.GOO or UnitType.cthulhu or UnitType.shub_niggurath or UnitType.nyarlathotep or UnitType.hastur or UnitType.king_in_yellow:
            self._goo.append(new_unit)

    def spend_power(self, cost):
        if self._power >= cost:
            self._power_spent = cost
            self._power -= self._power_spent
            return True
        else:
            print("Not enough power for action!")
            return False

    def recompute_power(self):
        self._power = self.current_cultists
        self._power += self.current_gates * 2

        for captive in self._captured_cultists:
            assert isinstance(captive, Unit)
            self._power += 1
            captive.set_unit_state(UnitState.in_reserve)
            captive.set_unit_zone(self._pool)
            self._captured_cultists.remove(captive)

        # add gates and special stuff.  This method will be overridden by faction specific thingies.
        pass

    def discover_possible_actions(self, map):
        possible_builds = self.find_build_actions()
        possible_moves = self.find_move_actions(map)
        possible_captures = self.find_capture_actions()
        possible_summons = self.find_summon_actions()
        possible_recruits = self.find_recruit_actions()
        '''
        PROBABALISTIC PLAYOUT
        assign a weight to each possible action type
        then select a specific action to execute
        multiple moves can happen at once
        Awesome AI logic goes here bro
        '''
        action_func = {
            'capture': [],
            'summon': [],
            'move': [],
            'build': [],
            'recruit': [],
            'combat': [],
            'awaken': [],
            'special': []
        }

        action_probability = {}

        if len(possible_captures) > 0:
            action_probability['capture'] = []
            action_probability['capture'].append(self.probability_dict['capture'])
            action_func['capture'] = possible_captures

        if len(possible_summons) > 0:
            action_probability['summon'] = []
            action_probability['summon'].append(self.probability_dict['summon'])
            action_func['summon'] = possible_summons

        if len(possible_moves) > 0:
            action_probability['move'] = []
            action_probability['move'].append(self.probability_dict['move'])
            action_func['move'] = possible_moves

        if len(possible_builds) > 0:
            action_probability['build'] = []
            action_probability['build'].append(self.probability_dict['build'])
            action_func['build'] = possible_builds

        if len(possible_recruits) > 0:
            action_probability['recruit'] = []
            action_probability['recruit'].append(self.probability_dict['recruit'])
            action_func['recruit'] = possible_recruits

        action_success = False
        while action_success is False:
            if len(action_probability) > 0:
                key_list = []
                p_dist = []

                for k, v in action_probability.iteritems():
                    p_dist.append(v[0])
                    key_list.append(k)

                p_norm = [float(i) / sum(p_dist) for i in p_dist]
                action = choice(range(len(key_list)), 1, p=p_norm)[0]

                action_params = action_func[key_list[action]][0]

                action_func.pop(key_list[action])
                action_probability.pop(key_list[action])

                if key_list[action] is 'capture':
                    action_success = self.capture_unit(action_params[0], action_params[1], action_params[2])
                if key_list[action] is 'move':
                    # TODO:  allow multiple moves
                    action_success = self.move_action(action_params[0], action_params[1], action_params[2])
                if key_list[action] is 'build':
                    action_success = self.build_gate_action(action_params[0], action_params[1])
                if key_list[action] is 'summon':
                    # TODO:  allow multiple summons for black goat with Fertility Cult
                    action_success = self.summon_action(action_params[0], action_params[1])
                if key_list[action] is 'recruit':
                    action_success = self.recruit_cultist(action_params[1])

            else:
                print("No Possible Actions!")
                self.spend_power(self.power)
                action_success = True
                return False

    def summon_action(self, monster, unit_zone):
        assert isinstance(monster, Unit)
        if monster.unit_state is UnitState.in_reserve:
            if self.spend_power(monster.cost):
                monster.set_unit_state(UnitState.in_play)
                monster.set_unit_zone(unit_zone)
                print(self._color + "A %s has appeared in %s" % (
                    monster.unit_type.value, monster.unit_zone.name) + TextColor.ENDC)
                return True
        return False

    def awaken_goo(self):
        return False

    def find_recruit_actions(self):
        # cultists can be recruited anywhere there is a unit
        recruit_actions = []
        for unit in self._units:
            assert isinstance(unit, Unit)
            if unit.unit_state is UnitState.in_play:
                for cultist in self._cultists:
                    if cultist.unit_state is UnitState.in_reserve:
                        if self.power >= cultist.cost:
                            recruit_actions.append((cultist, unit.unit_zone, None))
        return recruit_actions

    '''
    returns a list of tuples representing summon actions
    (UNIT, ZONE, NONE) units that can be summoned and where on the map they can be summoned
    '''

    def find_summon_actions(self):
        summon_actions = []
        # TODO: Black Goat needs to override this because of Fertility Cult and Red Sign
        # monsters can be summoned only at occupied gates
        for unit in self._units:
            assert isinstance(unit, Unit)
            if unit.gate_state is GateState.occupied and unit.unit_state is UnitState.in_play:
                for monster in self._monsters:
                    if monster.unit_state is UnitState.in_reserve:
                        if self.power >= monster.cost:
                            summon_actions.append((monster, unit.unit_zone, None))
        return summon_actions

    def find_capture_actions(self):
        capture_actions = []
        n = 0
        for monster in self._monsters:
            assert isinstance(monster, Unit)
            if monster.unit_state is UnitState.in_play:
                for unit in monster.unit_zone.occupancy_list:
                    if unit.unit_type is UnitType.cultist and unit.unit_state is UnitState.in_play:
                        if unit.faction._name != self._name:
                            capture_actions.append((monster, unit.unit_zone, unit))
                            n += 1
        return capture_actions

    def find_build_actions(self):
        build_actions = []
        if self.power >= 3:
            for cultist in self.cultists_in_play:
                if cultist.gate_state is GateState.noGate and cultist.unit_zone.gate_state is GateState.noGate:
                    build_actions.append((cultist, cultist.unit_zone, None))
        return build_actions

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
                    assert isinstance(unit, Unit)
                    candidate_moves = []
                    # build list of possible moves to neighboring zones
                    neighbors = map.find_neighbors(unit.unit_zone.name, unit.base_movement)
                    for n in neighbors:
                        candidate_moves.append((unit, unit.unit_zone, map.zone_by_name(n)))
                        all_possible_moves.append((unit, unit.unit_zone, map.zone_by_name(n)))

                elif unit.gate_state is GateState.occupied:
                    print(self._color + '%s %s in %s is maintaining a gate' % (
                        self._faction.value, unit.unit_type.value, unit.unit_zone.name) + TextColor.ENDC)
        return all_possible_moves

    def move_action(self, unit, from_zone, to_zone):
        assert isinstance(from_zone, Zone)
        assert isinstance(to_zone, Zone)
        '''
        Handles Zone and power transactions
        '''
        if self.spend_power(1):
            print(self._color + '%s %s is moving from %s to %s' % (
                self._faction.value, unit.unit_type.value, from_zone.name, to_zone.name) + TextColor.ENDC)
            from_zone.remove_unit(unit)
            unit.set_unit_zone(to_zone)
            self.capture_gate(unit)
            return True
        return False

    def combat_action(self):
        return False

    def build_gate_action(self, unit, zone):
        zone_state = zone.get_zone_state()
        action_cost = 3
        if zone_state[0] == GateState.noGate and unit.unit_state is UnitState.in_play:
            if self.spend_power(action_cost):
                print(self._color + '%s %s has built a gate in %s' % (
                    self._faction.value, unit.unit_type.value, zone.name) + TextColor.ENDC)
                zone.set_gate_state(GateState.occupied)
                zone.set_gate_unit(unit)
                unit.set_unit_gate_state(GateState.occupied)
                self._current_gates += 1
                return True
        else:
            print ('Gate already exists!')
            return False
        return False

    def take_spell_book(self):
        pass

    def spell_book_action(self):
        pass

    def pre_combat_action(self):
        pass

    def post_combat_action(self):
        pass

    def pre_doom_action(self):
        pass

    def post_doom_action(self):
        pass

    def pre_turn_action(self):
        pass

    def post_turn_action(self):
        pass

    def print_state(self):
        print (self._color)
        print ("**************************************")
        print ('name: %s' % self._name)
        print ('faction: %s' % self._faction)
        print ('home zone: %s' % self._home_zone.name)
        print ('spells: %s' % self._spells)
        print ('units: ')
        for unit in self._units:
            print(
                '   ' + unit.unit_type.value + ' (' + str(unit.unit_state) + ', ' + str(unit.combat_power) + ', ' + str(
                    unit.unit_zone.name) + ')')
        print ('power: %s' % self._power)
        print ('doom points: %s' % self._doom_points)
        print ('elder sign points: %s' % self._elder_points)
        print ('starting cultists: %s' % self._starting_cultists)
        print ('current cultists: %s' % len(self.cultists_in_play))
        print ('current gates: %s' % self._current_gates)
        print ('total current units: %s' % self._units.__len__())
        print ("**************************************" + TextColor.ENDC)
