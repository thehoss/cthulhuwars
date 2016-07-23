from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction, Cultist
from cthulhuwars.Zone import Zone, GateState
from cthulhuwars.Maps import Map
from cthulhuwars.DiceRoller import DiceRoller
from cthulhuwars.Color import TextColor
from cthulhuwars.Color import NodeColor

# Generic Player class
# Overridden by faction specific subclasses
# home_zone left intentionally without default since the Board needs to pass in the
# Zone class instance from the map construction


class Player(object):
    def __init__(self, faction, home_zone, name='Player1'):
        assert isinstance(home_zone, Zone)
        self._name = name
        self._faction = faction
        self._home_zone = home_zone
        self._spells = []
        self._units = []
        self._cultists = []
        self._power = 8
        self._doom_points = 0
        self._elder_points = 0
        self._starting_cultists = 6
        self._current_cultists = 0
        self._captured_cultists = 0
        self._current_gates = 0
        self._color = TextColor.GREEN
        self.node_color = NodeColor.GREEN

    def player_setup(self):
        # add starting gate and cultist to home zone
        # add remaining cultists
        for _ in range(self._starting_cultists):
            new_cultist = Cultist(self, self._home_zone, UnitState.in_play)
            self.add_unit(new_cultist)
            self._cultists.append(new_cultist)
        self.build_gate_action(self._cultists[0], self._home_zone)

    def summon_cultist(self, unit_zone):
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
        if unit.unit_type is UnitType.cultist:
            unit.faction.remove_cultist()
        unit.set_unit_state(UnitState.killed)

    def remove_unit(self, unit):
        assert isinstance(unit, Unit)
        if unit.unit_type is UnitType.cultist:
            unit.faction.remove_cultist()
        unit.set_unit_state(UnitState.in_reserve)

    def capture_unit(self, unit):
        assert isinstance(unit, Unit)
        if unit.unit_type is UnitType.cultist:
            unit.faction.remove_cultist()
        unit.set_unit_state(UnitState.in_reserve)
        self._captured_cultists += 1

    @property
    def power(self):
        return self._power

    @property
    def faction(self):
        return self._faction

    @property
    def current_cultists(self):
        return self._current_cultists

    @property
    def captured_cultists(self):
        return self._captured_cultists

    @property
    def current_gates(self):
        return self._current_gates

    def remove_cultist(self):
        self._current_cultists -= 1

    def add_unit(self, new_unit):
        self._units.append(new_unit)

    def spend_power(self, cost):
        if self._power >= cost:
            self._power -= cost
            return True
        else:
            print("Not enough power for action!")
            return False

    def recompute_power(self):
        self._current_cultists = 0
        for cultist in self._cultists:
            if cultist.unit_state is UnitState.in_play:
                self._current_cultists += 1
        self._power = self._current_cultists
        self._power += self._current_gates * 2
        # add gates and special stuff.  This method will be overridden by faction specific thingies.
        pass

    def find_move_actions(self, map):
        assert isinstance(map, Map)
        # we need to know who can move and to where
        # power determines how many moves we can make
        # after moving we also need to check for spell book
        # availability at 4 6 and 8 unique occupied zones
        occupied_zones = []
        for unit in self._units:
            if unit.unit_state is UnitState.in_play:
                assert isinstance(unit, Unit)
                candidate_moves = []
                occupied_zones.append(unit.unit_zone)
                # build list of possible moves to neighboring zones
                neighbors = map.find_neighbors(unit.unit_zone.name)
                for n in neighbors:
                    candidate_moves.append((unit, unit.unit_zone, map.zone_by_name(n)))
                #print(self._color+'%s %s in %s can make %s moves'%(self._faction, unit.unit_type, unit.unit_zone.name, neighbors._len__())+text_colors.ENDC)

                '''
                RANDOM PLAYOUT
                roll a die of with sides corresponding to legal moves and pick one
                will not roll if unit is occupying a gate
                Awesome AI logic goes here bro
                '''
                if unit.gate_state is GateState.occupied:
                    print(self._color + '%s %s in %s is maintaining a gate' % (self._faction.value, unit.unit_type.value, unit.unit_zone.name) + TextColor.ENDC)
                else:
                    dice = DiceRoller(1,neighbors.__len__()-1)
                    dice_result = int(dice.roll_dice()[0])
                    self.move_action(unit, unit.unit_zone, candidate_moves[dice_result][2])
        occupied_zones = list(set(occupied_zones))

    def move_action(self, unit, from_zone, to_zone):
        assert isinstance(from_zone, Zone)
        assert isinstance(to_zone, Zone)
        '''
        Handles Zone and power transactions
        '''
        if self.power >= 1:
            print(self._color + '%s %s is moving from %s to %s' % (self._faction.value, unit.unit_type.value, from_zone.name, to_zone.name) + TextColor.ENDC)
            from_zone.remove_unit(unit)
            unit.set_unit_zone(to_zone)
            #to_zone.add_unit(unit)
            self.spend_power(1)

    def combat_action(self):
        pass

    def build_gate_action(self, unit, zone):
        zone_state = zone.get_zone_state()
        action_cost = 2
        if zone_state[0] == GateState.noGate:
            if self.spend_power(action_cost):
                zone.set_gate_state(GateState.occupied)
                zone.set_gate_unit(unit)
                unit.set_unit_gate_state(GateState.occupied)
                self._current_gates += 1
        else:
            print ('Gate already exists!')

    def spell_book_action(self):
        pass

    def summon_action(self):
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
              print('   '+unit.unit_type.value + ' ('+str(unit.unit_state)+', '+str(unit.combat_power)+', '+str(unit.unit_zone.name)+')')
        print ('power: %s' % self._power)
        print ('doom points: %s' % self._doom_points)
        print ('elder sign points: %s' % self._elder_points)
        print ('starting cultists: %s' % self._starting_cultists)
        print ('current cultists: %s' % self._current_cultists)
        print ('current gates: %s' % self._current_gates)
        print ('total current units: %s' % self._units.__len__())
        print ("**************************************" + TextColor.ENDC)
