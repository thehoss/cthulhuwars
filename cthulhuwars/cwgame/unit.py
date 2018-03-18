from enum import Enum
from .zone import Zone, GateState

class UnitType(Enum):
    cultist = 'cultist'
    monster = 'monster'
    GOO = 'Great Old One'
    terror = 'terror'
    dark_young = 'dark young'
    ghoul = 'ghoul'
    fungi = 'fungi'
    deep_one = 'deep one'
    shoggoth = 'shoggoth'
    star_spawn = 'star spawn'
    flying_polyp = 'flying polyp'
    nightgaunt = 'nightgaunt'
    hunting_horror = 'hunting horror'
    undead = 'undead'
    byakhee = 'byakhee'
    king_in_yellow = 'king in yellow'
    hastur = 'hastur'
    shub_niggurath = 'shub-niggurath'
    cthulhu = 'cthulhu'
    nyarlathotep = 'nyarlathotep'

class UnitState(Enum):
    in_reserve = 0
    in_play = 1
    killed = 2
    captured = 3

class Faction(Enum):
    cthulhu = 'cthulhu'
    black_goat = 'black_goat'
    crawling_chaos = 'crawling_chaos'
    yellow_sign = 'yellow_sign'
    sleeper = 'sleeper'
    windwalker = 'windwalker'
    opener_of_the_way = 'opener_of_the_way'
    tcho_tcho = 'tcho_tcho'
    azathoth = 'azathoth'

class Unit(object):
    def __init__(self, faction, unit_zone, unit_type=UnitType.cultist, combat_power=0, cost=1, base_movement=1,
                 unit_state=UnitState.in_reserve):
        self._faction = faction
        self._unit_type = unit_type
        self._combat_power = combat_power
        self._cost = cost
        self._base_movement = base_movement
        self._unit_state = unit_state
        self._unit_zone = unit_zone
        self._unit_gate_state = GateState.noGate

        self.set_unit_zone(unit_zone)
        #print('New %s unit in %s' % (self.__unit_type, self.__unit_zone.name))

    @property
    def unit_zone(self):
        return self._unit_zone

    def set_unit_zone(self, unit_zone):
        assert isinstance(unit_zone, Zone)
        self._unit_zone.remove_unit(self)
        self._unit_zone = unit_zone
        unit_zone.add_unit(self)

    @property
    def faction(self):
        return self._faction

    @property
    def unit_type(self):
        return self._unit_type

    @property
    def type(self):
        return self._unit_type

    def set_unit_type(self, unit_type):
        self._unit_type = unit_type

    @property
    def gate_state(self):
        return self._unit_gate_state

    def set_unit_gate_state(self, gate_state):
        self._unit_gate_state = gate_state

    @property
    def combat_power(self):
        return self._combat_power

    def set_combat_power(self, combat_power):
        self._combat_power = combat_power

    @property
    def cost(self):
        return self._cost

    def set_cost(self, cost):
        self._cost = cost

    @property
    def base_movement(self):
        return self._base_movement

    def set_base_movement(self, base_movement):
        self._base_movement = base_movement

    @property
    def unit_state(self):
        return self._unit_state

    def set_unit_state(self, unit_state):
        self._unit_state = unit_state

    def return_to_pool(self):
        self.set_unit_zone(self._faction._pool)
        self.set_unit_state(UnitState.in_reserve)

    def render_unit(self):
        render_definition = {
            "nodetype": ["sphere"],
            "name": ["%s_%s_%s"%(self.faction._name, self._unit_type.value, self.id())],
            "params": [("float", "radius", 0.015)]
        }
        return render_definition

class Cultist(Unit):
    def __init__(self, faction, unit_zone, base_movement, unit_state):
        super(Cultist, self).__init__(faction, unit_zone, UnitType.cultist, 0, 1, base_movement, unit_state)

    def render_unit(self):
        render_definition = {
            "nodetype": ["procedural"],
            "name": ["cultist_object"],
            "params": [("string", "dso", "cultist.obj"),
                       ("bool", "load_at_init", 1)]
        }
        return render_definition

class Monster(Unit):
    def __init__(self, faction, unit_zone, unit_type = UnitType.monster, combat_power=0, cost=1, base_movement=1, unit_state = UnitState.in_reserve):
        super(Monster, self).__init__(faction, unit_zone, unit_type, combat_power, cost, base_movement, unit_state)


class GreatOldOne(Unit):
    def __init__(self, faction, unit_zone, unit_type = UnitType.GOO, combat_power=0, cost=1, base_movement=1, unit_state = UnitState.in_reserve):
        super(GreatOldOne, self).__init__(faction, unit_zone, unit_type, combat_power, cost, base_movement, unit_state)
