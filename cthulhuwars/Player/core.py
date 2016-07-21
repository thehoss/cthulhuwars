from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction, Cultist
from cthulhuwars.Zone import Zone, GateState
from cthulhuwars.Maps import Map
from cthulhuwars.DiceRoller import DiceRoller
# Generic Player class
# Overridden by faction specific subclasses
# home_zone left intentionally without default since the Board needs to pass in the
# Zone class instance from the map construction
class text_colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Player(object):
    def __init__(self, faction, home_zone, name='Player1'):
        assert isinstance(home_zone, Zone)

        self.__name = name
        self.__faction = faction
        self.__home_zone = home_zone
        self.__spells = []
        self.__units = []
        self.__power = 8
        self.__doom_points = 0
        self.__elder_points = 0
        self.__starting_cultists = 6
        self.__current_cultists = 0
        self.__current_gates = 0
        self._color = text_colors.GREEN

    def player_setup(self):
        # add starting gate and cultist to home zone
        self.build_gate_action(self._add_cultist(self.__home_zone), self.__home_zone)
        # add remaining cultists
        for _ in range(1, self.__starting_cultists, 1):
            self._add_cultist(self.__home_zone)

    def _add_cultist(self, zone):
        if self.__power > 0:
            new_cultist = Cultist(self, zone, UnitState.in_play)
            self.__units.append(new_cultist)
            self.__power -= 1
            self.__current_cultists += 1
            return new_cultist
        elif self.__power < 1:
            # TODO: add failure reporting mechanism
            print ('not enough power to summon cultist!')

    @property
    def power(self):
        return self.__power

    @property
    def faction(self):
        return self.__faction

    def add_unit(self, new_unit, unit_cost):
        self.__units.append(new_unit)
        self.__power -= unit_cost

    def recompute_power(self):
        self.__power = self.__current_cultists
        self.__power += self.__current_gates * 2
        # add gates and special stuff.  This method will be overridden by faction specific thingies.
        pass

    def find_move_actions(self, map):
        assert isinstance(map, Map)
        # we need to know who can move and to where
        # power determines how many moves we can make
        # after moving we also need to check for spell book
        # availability at 4 6 and 8 unique occupied zones
        occupied_zones = []
        power = self.power
        for unit in self.__units:
            candidate_moves = []
            assert isinstance(unit, Unit)
            occupied_zones.append(unit.unit_zone)
            # build list of possible moves to neighboring zones
            neighbors = map.find_neighbors(unit.unit_zone.name)
            for n in neighbors:
                candidate_moves.append((unit, unit.unit_zone, map.zone_by_name(n)))
            #print(self._color+'%s %s in %s can make %s moves'%(self.__faction, unit.unit_type, unit.unit_zone.name, neighbors.__len__())+text_colors.ENDC)

            '''
            RANDOM PLAYOUT
            roll a die of with sides corresponding to legal moves and pick one
            will not roll if unit is occupying a gate
            Awesome AI logic goes here bro
            '''
            if unit.gate_state is GateState.occupied:
                print(self._color + '%s %s in %s is maintaining a gate' % (self.__faction, unit.unit_type, unit.unit_zone.name) + text_colors.ENDC)
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
            print(self._color + '%s %s is moving from %s to %s' % (self.__faction, unit.unit_type, from_zone.name, to_zone.name) + text_colors.ENDC)
            from_zone.remove_unit(unit)
            to_zone.add_unit(unit)
            self.__power -= 1

    def combat_action(self):
        pass

    def build_gate_action(self, unit, zone):
        zone_state = zone.get_zone_state()
        if zone_state[0] == GateState.noGate:
            if self.power >= 2:
                zone.set_gate_state(GateState.occupied)
                zone.set_gate_unit(unit)
                unit.set_unit_gate_state(GateState.occupied)
                self.__current_gates += 1
                self.__power -= 2
            else:
                print ('Not enough power to build gate!')
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
        print ("**************************************")
        print ('name: %s' % self.__name)
        print ('faction: %s' % self.__faction)
        print ('home zone: %s' % self.__home_zone.name)
        print ('spells: %s' % self.__spells)
        unit_string = ', '.join(unit.unit_type for unit in self.__units)
        print ('units: %s'%unit_string)
        print ('power: %s' % self.__power)
        print ('doom points: %s' % self.__doom_points)
        print ('elder sign points: %s' % self.__elder_points)
        print ('starting cultists: %s' % self.__starting_cultists)
        print ('current cultists: %s' % self.__current_cultists)
        print ('current gates: %s' % self.__current_gates)
        print ('total current units: %s' % self.__units.__len__())
        print ("**************************************" + text_colors.ENDC)
