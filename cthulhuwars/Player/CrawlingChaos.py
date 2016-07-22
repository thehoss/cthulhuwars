from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState
from cthulhuwars.Maps import Map
from cthulhuwars.DiceRoller import DiceRoller

#  Crawling Chaos
#  Starts in Asia or East Asia
#
class text_colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CrawlingChaos(Player):
    def __init__(self, home_zone, name='The Crawling Chaos'):
        super(CrawlingChaos, self).__init__(Faction.crawling_chaos, home_zone, name)
        self._nightgaunt_in_play = 0
        self._flying_polyp_in_play = 0
        self._hunting_horror_in_play = 0
        self._nyarlathotep_in_play = 0
        self._spell_emmisary_of_the_outer_gods = False
        self._spell_abduct = False
        self._spell_madness = False
        self._spell_the_thousand_forms = False
        self._spell_seek_and_destroy = False
        self._spell_invisibility = False
        self._color = text_colors.BLUE

    def find_move_actions(self, map):
        assert isinstance(map, Map)
        # we need to know who can move and to where
        # power determines how many moves we can make
        # after moving we also need to check for spell book
        # availability at 4 6 and 8 unique occupied zones
        occupied_zones = []
        power = self.power
        for unit in self._units:
            candidate_moves = []
            assert isinstance(unit, Unit)
            occupied_zones.append(unit.unit_zone)
            # build list of possible moves to neighboring zones
            # Crawling Chaos' special ability:  units are able to travel up to 2 Zones
            neighbors = map.find_neighbors(unit.unit_zone.name, 2)
            for n in neighbors:
                candidate_moves.append((unit, unit.unit_zone, map.zone_by_name(n)))
            #print(self._color+'%s %s in %s can make %s moves'%(self._faction, unit.unit_type, unit.unit_zone.name, neighbors.__len__())+text_colors.ENDC)

            '''
            RANDOM PLAYOUT
            roll a die of with sides corresponding to legal moves and pick one
            will not roll if unit is occupying a gate
            Awesome AI logic goes here bro
            '''
            if unit.gate_state is GateState.occupied:
                print(self._color + '%s %s in %s is maintaining a gate' % (self._faction, unit.unit_type, unit.unit_zone.name) + text_colors.ENDC)
            else:
                dice = DiceRoller(1,neighbors.__len__()-1)
                dice_result = int(dice.roll_dice()[0])
                self.move_action(unit, unit.unit_zone, candidate_moves[dice_result][2])
        occupied_zones = list(set(occupied_zones))

    def print_state(self):
        print (self._color)
        super(CrawlingChaos,self).print_state()


class Nightgaunt(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost):
        super(Nightgaunt, self).__init__(unit_parent, unit_zone, UnitType.monster, combat_power=0, cost=unit_cost,
                                        base_movement=2,
                                        unit_state=UnitState.in_reserve)
class FlyingPolyp(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost):
        super(FlyingPolyp, self).__init__(unit_parent, unit_zone, UnitType.monster, combat_power=1, cost=unit_cost,
                                        base_movement=2,
                                        unit_state=UnitState.in_reserve)

class HuntingHorror(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost):
        super(HuntingHorror, self).__init__(unit_parent, unit_zone, UnitType.monster, combat_power=2, cost=unit_cost,
                                        base_movement=2,
                                        unit_state=UnitState.in_reserve)
