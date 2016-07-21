from enum import Enum
from cthulhuwars.Zone import Zone, GateState


class UnitType(Enum):
    cultist = 'cultist'
    monster = 'monster'
    GOO = 'Great Old One'


class Faction(Enum):
    cthulhu = 'Cthulhu'
    black_goat = 'Black Goat'
    crawling_chaos = 'Crawling Chaos'
    yellow_sign = 'Yellow Sign'
    sleeper = 'Sleeper'
    windwalker = 'Windwalker'
    opener_of_the_way = 'Opener of the Way'
    tcho_tcho = 'Tcho Tcho'
    azathoth = 'Azathoth'


class UnitState(Enum):
    in_reserve = 0
    in_play = 1
    killed = 2
    captured = 3


class Unit(object):
    def __init__(self, faction, unit_zone, unit_type=UnitType.cultist, combat_power=0, cost=1, base_movement=1,
                 unit_state=UnitState.in_reserve):
        self.__faction = faction
        self.__unit_type = unit_type
        self.__combat_power = combat_power
        self.__cost = cost
        self.__base_movement = base_movement
        self.__unit_state = unit_state
        self.__unit_zone = unit_zone
        self.__unit_gate_state = GateState.noGate

        assert isinstance(unit_zone, Zone)
        unit_zone.add_unit(self)

        #print('New %s unit in %s' % (self.__unit_type, self.__unit_zone.name))

    @property
    def unit_zone(self):
        return self.__unit_zone

    @property
    def faction(self):
        return self.__faction

    @property
    def unit_type(self):
        return self.__unit_type

    def set_unit_type(self, unit_type):
        self.__unit_type = unit_type

    def set_unit_gate_state(self, gate_state):
        self.__unit_gate_state = gate_state

    @property
    def combat_power(self):
        return self.__combat_power

    def set_combat_power(self, combat_power):
        self.__combat_power = combat_power

    @property
    def cost(self):
        return self.__cost

    def set_cost(self, cost):
        self.__cost = cost

    @property
    def base_movement(self):
        return self.__base_movement

    def set_base_movement(self, base_movement):
        self.__base_movement = base_movement

    @property
    def unit_state(self):
        return self.__unit_state

    def set_unit_state(self, unit_state):
        self.__unit_state = unit_state


class Cultist(Unit):
    def __init__(self, faction, unit_zone, unit_state):
        super(Cultist, self).__init__(faction, unit_zone, UnitType.cultist, 0, 1, 1, unit_state)


class Monster(Unit):
    def __init__(self, faction, unit_zone, unit_state):
        super(Monster, self).__init__(faction, unit_zone, UnitType.monster, 0, 1, 1, unit_state)


class GreatOldOne(Unit):
    def __init__(self, faction, unit_zone, unit_state):
        super(GreatOldOne, self).__init__(faction, unit_zone, UnitType.GOO, 0, 1, 1, unit_state)

