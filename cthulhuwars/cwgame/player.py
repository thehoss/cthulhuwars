from .color import TextColor, NodeColor
from .diceRoller import DiceRoller
from .map import Map
from .playerLogic import PlayerLogic
from .unit import Unit, UnitType, UnitState, Faction, Cultist
from .zone import Zone, GateState
import itertools
from collections import defaultdict
from .combinatorics import unlabeled_balls_in_labeled_boxes


# Generic Player class
# Overridden by faction specific subclasses
# home_zone left intentionally without default since the Board needs to pass in the
# Zone class instance from the map construction

'''
    AStarks:
    For moving Cultists? Only move into areas lacking both a gate and a cultist belonging 
    to a faction with 3+ power, that also aren't within reach of an enemy Monster/Terror/GOO 
    who's owner has enough power to reach said Cultist in 1 Turn (that is to say, Submerge 
    doesn't factor in) Though that means once Hastur and King in Yellow are in play, no area is safe
    Plus, Dreams makes the gate construction dangerous
    So, for both of those, you'd also have the restriction of needing to move 2 Cultists in

    All factions have a movement or "movement" cheapener.
    Avatar, necrophagy, ice age, burrow, submerge, etc
'''


class Player(object):
    def __init__(self, faction, home_zone, board, name='Player1'):
        assert isinstance(home_zone, Zone)

        self._name = name
        self._faction = faction
        self._home_zone = home_zone
        self._spells = 0
        self._spell_requirement_met = [False] * 6
        self._units = set()
        self._cultists = set()
        self._monsters = set()
        self._goo = set()
        self._power = 8
        self._power_spent = 0
        self._doom_points = 0
        self._elder_points = 0
        self._starting_cultists = 6
        self._current_cultists = 0
        self._captured_cultists = set()
        self._current_gates = 0
        self._occupied_zones = set()
        self._color = TextColor.GREEN
        self._node_color = NodeColor.GREEN

        self.brain = PlayerLogic(self, board.map)

        self.brain.use_method_wc()
        '''
            probability_dict
            This dictionary sets up the probability that a player will execute a
            particular action on a turn.  This is used in the PlayerLogic class
            Probabilities are normalized later and can be should be modified
            by various factors
        '''
        self.probability_dict = {
            'capture': 0.225,
            'build': 0.225,
            'move': 0.15,
            'summon': 0.175,
            'recruit': 0.125,
            'combat': 0.1,
            'awaken': 0.0,
            'special': 0.0
        }
        self.brain.set_probabilities(self.probability_dict)

        '''
            board
            instance of the game
        '''
        self._board = board
        '''
            pool
            This is a generic 'blank' zone where units not in play are kept
        '''
        self._pool = Zone('pool')

    def player_setup(self):
        # reset the entire faction
        # add starting gate and cultist to home zone
        # add remaining cultists
        del self._cultists
        del self._current_gates
        del self._goo
        del self._units
        del self._monsters

        self._spells = 0
        self._spell_requirement_met = [False] * 6

        self._units = set()
        self._cultists = set()
        self._monsters = set()
        self._goo = set()
        self._power = 8
        self._power_spent = 0
        self._doom_points = 0
        self._elder_points = 0
        self._starting_cultists = 6
        self._current_cultists = 0
        self._captured_cultists = set()
        self._current_gates = 0
        self._occupied_zones = set()

        self._base_movement = 1
        if self._faction == Faction.crawling_chaos:
            self._base_movement = 2
        for _ in range(self._starting_cultists):
            new_cultist = Cultist(self, self._home_zone, self._base_movement, UnitState.in_play)
            self.add_unit(new_cultist)
            self._cultists.add(new_cultist)
        self.build_gate_action(list(self._cultists)[0], self._home_zone)
        self.compute_influence_map(self._board.map)

    def pprint(self, msg):
        print(self._color + TextColor.BOLD + msg + TextColor.ENDC)

    '''
     sacrifice_unit
     remove a unit from the map and place it in the owners pool
     '''

    def sacrifice_unit(self, unit):
        assert isinstance(unit, Unit)
        unit.set_unit_state(UnitState.in_reserve)
        unit.set_unit_zone(self._pool)
        return True

    '''
    remove_unit
    same as above, however removal may only be temporary, versus kill
    '''

    def remove_unit(self, unit):
        assert isinstance(unit, Unit)
        unit.set_unit_state(UnitState.in_reserve)
        unit.set_unit_zone(self._pool)
        return True

    '''
    capture_unit
    only cultists can be captured and only monsters may do the capturing
    '''

    def capture_unit(self, monster, unit_zone, unit):
        assert isinstance(unit, Unit)
        assert isinstance(monster, Unit)
        assert isinstance(unit_zone, Zone)

        if unit.unit_type is UnitType.cultist:
            if self.spend_power(1):
                print(self._color + TextColor.BOLD + "%s %s has captured %s %s in %s" % (
                    self._name, monster.unit_type.value, unit.faction._name, unit.unit_type.value,
                    unit.unit_zone.name) + TextColor.ENDC)
                if unit.gate_state is GateState.occupied:
                    unit.set_unit_gate_state(GateState.noGate)
                    unit_zone.clear_gate_state()
                    self.capture_gate(monster)
                self._captured_cultists.add(unit)
                unit.set_unit_state(UnitState.captured)
                unit.set_unit_zone(self._pool)
                return True
        return False

    '''
    occupied_zones property
    returns a list of unique zones occupied by this player
    '''

    @property
    def occupied_zones(self):
        self._occupied_zones = []
        for unit in self._units:
            if unit.unit_state is UnitState.in_play:
                self._occupied_zones.append(unit.unit_zone)
        self._occupied_zones = list(set(self._occupied_zones))
        return self._occupied_zones

    '''
    power property
    returns the current power value of this player
    '''

    @property
    def power(self):
        return self._power

    @property
    def name(self):
        return self._name

    @property
    def short_name(self):
        return self._faction.value
    '''
    faction property
    returns the faction enum, defined in Unit, of the current player
    '''

    @property
    def faction(self):
        return self._faction

    '''
    current_cultists property
    returns the number of cultists currently in play
    '''

    @property
    def current_cultists(self):
        self._current_cultists = len(self.cultists_in_play)
        return self._current_cultists

    '''
    cultists_in_play property
    returns a list of Cultist units that are currently on the map
    '''

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

    '''
    units_in_play property
    returns a list of units that are currently on the map
    '''

    @property
    def units_in_play(self):
        units_in_play = []
        for c in self._units:
            if c.unit_zone is not self._pool and c.unit_state is UnitState.in_play:
                units_in_play.append(c)
        return units_in_play

    '''
    captured_cultists
    return the number of cultists captured by this player
    '''

    @property
    def captured_cultists(self):
        return len(self._captured_cultists)

    '''
    current_gates
    return the number of gates this player controls
    BlackGoat overrides this to account for Dark Young with her Red Sign spell
    '''

    @property
    def current_gates(self):
        gates = 0
        for cultist in self.cultists_in_play:
            if cultist.gate_state is GateState.occupied and cultist.unit_zone is not self._pool:
                gates += 1
        self._current_gates = gates
        return self._current_gates

    @property
    def doom_points(self):
        dp = self.current_gates
        self._doom_points += dp
        return dp

    @property
    def elder_points(self):
        return self._elder_points

    '''
    abandon_gate
    unit occupying the gate leaves the gate, presumably to move to another zone
    '''

    def abandon_gate(self, unit):
        assert isinstance(unit, Cultist)
        if unit.gate_state is GateState.occupied:
            unit.set_unit_gate_state(GateState.noGate)
            unit.unit_zone.clear_gate_state()
            self._current_gates -= 1
            return True
        return False

    '''
    capture_gate
    cultist unit in a zone with an unoccupied gate can take control of the gate at no cost
    BlackGoat overrides this method to account for Dark Young with Red Sign spell
    '''

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

    '''
    free_action
    the free action method implements logic that costs 0 power and is labeled a free action
    It runs before and after every turn
    '''

    def free_action(self):
        for unit in self.units_in_play:
            self.capture_gate(unit)

    '''
    add_unit
    adds a new unit to the player pool and updates _monsters and _goo lists
    '''

    def add_unit(self, new_unit):
        self._units.add(new_unit)
        if new_unit.unit_type is not UnitType.cultist:
            self._monsters.add(new_unit)
        if new_unit.unit_type is UnitType.GOO or UnitType.cthulhu or UnitType.shub_niggurath or UnitType.nyarlathotep or UnitType.hastur or UnitType.king_in_yellow:
            self._goo.add(new_unit)

    '''
    spend_power
    account for the use of power to execute actions.  Will fail if power is insufficient for transaction
    this method should be called whenever power is needed by an action or spell
    '''

    def spend_power(self, cost):
        if self._power >= cost:
            self._power_spent = cost
            self._power -= self._power_spent
            return True
        else:
            print("Not enough power for action!")
            return False

    '''
    recompute_power
    given the current state of the map and players, compute the total power gained for this player
    this method is called whenever a new round begins, as part of the Gather Power phase
    '''

    def recompute_power(self):
        self._power = self.current_cultists
        self._power += self.current_gates * 2
        self._power += len(self._board.map.empty_gates)

        for captive in self._captured_cultists:
            assert isinstance(captive, Unit)
            self._power += 1
            captive.return_to_pool()
        self._captured_cultists.clear()

        # add gates and special stuff.  This method will be overridden by faction specific thingies.
        pass

    '''
    compute_influence_map
    
    influence:
        my_influence
        opponent(s)_influence
        
        derived:
        influence        (my_influence - sum(opponents_influence))
                                         max(opponents_influence)
                                         min(opponents_influence)
                                         mean(opponents_influence)
                                         ...
        tension          (my_influence + sum(opponents_influence))
                          ...
                          
        vulnerability    (tension - abs(influence))
                         (tension - abs(...))
        
        ...
        one of n-way influence  (my_influence - opponent[n]_influence)        
        one of n-way tension    (my_influence + opponent[n]_influence)
    '''

    def compute_influence_map(self, map):
        assert isinstance(map, Map)

        # here, self.power-1 assumes a single zone move, with 1 power remaining to initiate battle
        # thus, with remaining power of 2, influence can only extend to immediately neighboring zones
        # might wanna just use self.power... dunno
        neighborhood_expansion = self._base_movement * min(max(self.power-1, 1), 2)

        all_zones = map.all_map_zones
        #print(self._faction)

        for zone in all_zones:
            zone.reset_influence(self.faction)

        my_zones = self.occupied_zones
        for zone in my_zones:
            candidate_units = self.my_units_in_zone(zone)
            #print(candidate_units)
            # tally units by base class
            tally_unit_supers = defaultdict(int)
            for unit in candidate_units:
                tally_unit_supers[type(unit).__bases__] += 1
                #tally_unit_supers[unit._unit_type] += 1

        for unit_super, value in tally_unit_supers.items():
            #print('unit super tally: %s  %s' % (unit_super, value))
            zone.set_influenceA(self.faction, unit_super, value)

        falloff_rate = 2
        for zone in my_zones:
            for n in range(1, neighborhood_expansion+1):
                neighbors_list = map.neighborhood(zone.name, n)
                for neighbor_zone_name in neighbors_list:
                    neighbor_zone = map.zone_by_name(neighbor_zone_name)
                    for unit_super, value in tally_unit_supers.items():
                        try:
                            influence_valueA = zone.get_influenceA(self.faction, unit_super) * 1.0 / pow(n+1, falloff_rate)
                        except KeyError:
                            influence_valueA = 0
                        try:
                            influence_valueB = neighbor_zone.get_influenceB(self.faction, unit_super)
                        except KeyError:
                            influence_valueB = 0
                        influence = influence_valueA + influence_valueB
                        #print(neighbor_zone, unit_super, influence)
                        neighbor_zone.set_influenceB(self.faction, unit_super, influence)

        for zone in all_zones:
            zone.copy_to_influenceA()

    '''
    find_recruit_actions
    returns a list of all possible recruit actions based on current state of units on the board
    this list is a tuple: (the cultist unit to be recruited, the zone in which to recruit, None)
    '''

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
    find_summon_actions
    returns a list of all possible summon actions based on current state of units and gates on the board
    this list is a tuple: (the unit to be summoned, the zone in which to summon, None)
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

    '''
    find_capture_actions
    returns a list of all possible capture actions based on current state of units on the board
    this list is a tuple: (the unit capturing, the zone in which the capture takes place, the unit to be captured)
    '''

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

    '''
    find_build_actions
    returns a list of all possible build actions based on current state of units and zones on the board
    this list is a tuple: (the unit building the gate, the zone in which to build, None)
    '''

    def find_build_actions(self):
        build_actions = []
        if self.power >= 3:
            for cultist in self.cultists_in_play:
                if cultist.gate_state is GateState.noGate and cultist.unit_zone.gate_state is GateState.noGate:
                    build_actions.append((cultist, cultist.unit_zone, None))
        return build_actions

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
                    score = 1
                    assert isinstance(unit, Unit)
                    if unit.unit_type is not UnitType.cultist:
                        score += 1
                    # build list of possible moves to neighboring zones
                    neighbors = map.find_neighbors(unit.unit_zone.name, unit.base_movement)
                    for n in neighbors:
                        destination_zone = map.zone_by_name(n)
                        assert isinstance(destination_zone, Zone)
                        if destination_zone.gate_state is GateState.emptyGate:
                            score += 2 
                        for occupant in destination_zone.occupancy_list:
                            assert isinstance(occupant, Unit)
                            if occupant.unit_type is UnitType.cultist and unit.unit_type is not UnitType.cultist:
                                score += 1
                            if occupant.unit_type is not UnitType.cultist and unit.unit_type is UnitType.cultist:
                                score -= 1

                        # if len(destination_zone.occupancy_list) == 0:
                        #    score += 1
                        all_possible_moves.append((unit, unit.unit_zone, destination_zone, score))

                if unit.gate_state is GateState.occupied:
                    pass
                    # print(self._color + '%s %s in %s is maintaining a gate' % (
                    #    self._faction.value, unit.unit_type.value, unit.unit_zone.name) + TextColor.ENDC)
        return all_possible_moves

    '''
     find_combat_action
     boilerplate combat action stub
     '''

    def find_combat_actions(self):
        combat_actions = []
        my_zones = self.occupied_zones
        for zone in my_zones:
            attackers = self.my_units_in_zone(zone)
            defenders = self.enemy_combatants_in_zone(zone)
            if len(defenders) > 0:
                defenderFaction = list(defenders)[0]._faction

                total_attack_power = self.determine_combat_power(list(attackers))
                total_defense_power = defenderFaction.determine_combat_power(list(defenders))

                # if total_attack_power > total_defense_power:
                score = total_attack_power - total_defense_power
                if len(attackers) > 0:
                    combat_actions.append((attackers, zone, defenders, score))
        return combat_actions

    '''
    find_special_actions
    stub for special faction actions, e.g. blood sacrifice
    '''

    def find_special_actions(self):
        return []

    '''
      summon_action
      boilerplate summon method.  each faction will override this to specific needs based on unit populations
      '''

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



    '''
    awaken_goo
    stub method for summoning great old ones
    '''

    def awaken_goo(self):
        return False

    '''
    move_action
    boilerplate move action method
    executes a move of unit from from_zone into to_zone
    '''

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

    '''
    draw_elder_sign
    draw one of three valued elder signs
    '''

    def draw_elder_sign(self):
        result = self._board.draw_elder_sign()
        self._elder_points += result
        return result


    '''
    combat_action
    boilerplate combat action
    '''

    def combat_action(self, attackers, zone, defenders):

        defenderFaction = defenders[0]._faction
        assert isinstance(defenderFaction, Player)

        total_attack_power = self.determine_combat_power(list(attackers))
        total_defense_power = defenderFaction.determine_combat_power(list(defenders))

        self.pre_combat_action()
        defenderFaction.pre_combat_action()

        if total_attack_power > 0:
            if self.spend_power(1):
                print(self._color + TextColor.BOLD + 'A battle has erupted in %s!' % (zone.name) + TextColor.ENDC)
                print(self._color + TextColor.BOLD + '     ' + ', '.join(
                    a.unit_type.value for a in attackers) + ' : %s' % total_attack_power + TextColor.ENDC)
                print(self._color + TextColor.BOLD + '     ' + ', '.join(
                    d.unit_type.value for d in defenders) + ' : %s' % total_defense_power + TextColor.ENDC)

                attack_dice = DiceRoller(total_attack_power)
                defence_dice = DiceRoller(total_defense_power)

                attack_rolls = attack_dice.interpret_dice()
                defence_rolls = defence_dice.interpret_dice()

                # print ('    attacker rolled: %s' % attack_rolls)
                # print ('    defender rolled: %s' % defence_rolls)

                for _ in range(attack_rolls['kill']):
                    # TODO: kill an enemy monster
                    defenders = self.brain.kill_from_selection(defenders)
                for _ in range(attack_rolls['pain']):
                    # TODO: force an enemy to move, defenders choice
                    defenders = self.brain.pain_from_selection(defenders)

                for _ in range(defence_rolls['kill']):
                    attackers = self.brain.kill_from_selection(attackers)
                    # TODO: kill an attackers monster
                for _ in range(defence_rolls['pain']):
                    # TODO: force an attacker to move, attackers choice
                    attackers = self.brain.pain_from_selection(attackers)

                return True

            self._board.post_combat_actions()

            return False

    '''
    determine the combat power of a group of units
    '''

    def determine_combat_power(self, units):
        total_combat_power = 0
        for unit in units:
            total_combat_power += unit.combat_power
        return total_combat_power

    def my_units_in_zone(self, zone):
        assert isinstance(zone, Zone)
        units_in_zone = []
        for unit in zone.occupancy_list:
            assert isinstance(unit, Unit)
            if unit.faction._name is self._name:
                units_in_zone.append(unit)
        return units_in_zone

    def enemy_units_in_zone(self, zone):
        assert isinstance(zone, Zone)
        units_in_zone = []
        for unit in zone.occupancy_list:
            assert isinstance(unit, Unit)
            if unit.faction._name is not self._name:
                units_in_zone.append(unit)
        return units_in_zone

    def enemy_combatants_in_zone(self, zone):
        assert isinstance(zone, Zone)
        units_in_zone = []
        for unit in zone.occupancy_list:
            assert isinstance(unit, Unit)
            if unit.faction._name is not self._name and unit.unit_type is not UnitType.cultist:
                units_in_zone.append(unit)
        return units_in_zone

    '''
    build_gate_action
    boilerplate build action.  will fail if a gate already exists or insufficient power
    '''

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

    '''
    recruit_cultist
    recruit a cultist from the pool onto the map
    '''

    def recruit_cultist(self, unit_zone):
        unit_cost = 1
        if self.power >= unit_cost:
            for cultist in self._cultists:
                if cultist.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        cultist.set_unit_state(UnitState.in_play)
                        cultist.set_unit_zone(unit_zone)
                        print(self._color + '%s has recruited a cultist in %s' % (
                            self._faction.value, unit_zone.name) + TextColor.ENDC)
                        return True
        return False

    def special_action(self, arguments):
        pass

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
        self.compute_influence_map(self._board.map)
        pass

    def faction_state(self):
        return (self._faction, self._power, self._spells, self._doom_points, self._elder_points)

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
        print ('current cultists: %s' % len(self.cultists_in_play))
        print ('current gates: %s' % self._current_gates)
        print ('total current units: %s' % self._units.__len__())
        print ("**************************************" + TextColor.ENDC)
