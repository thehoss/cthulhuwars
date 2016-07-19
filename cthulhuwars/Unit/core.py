from enum import Enum
from cthulhuwars.zone import Zone, GateState

class UnitType(Enum):
    cultist = 'cultist'
    monsterA = 'monsterA'
    monsterB = 'monsterB'
    monsterC = 'monsterC'
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
    in_play    = 1
    killed     = 2
    captured   = 3


class Unit:
    def __init__(self, faction=Faction.cthulhu, unit_type=UnitType.cultist, combat_power=0, cost=1,  base_movement=1,  unit_state=UnitState.in_reserve, unit_zone=Zone('South Pacific',True)):
        self.__faction = faction
        self.__unit_type = unit_type
        self.__combat_power = combat_power
        self.__cost = cost
        self.__base_movement = base_movement
        self.__unit_state = unit_state
        self.__unit_zone = unit_zone
        self.__unit_gate_state = GateState.noGate

        print('New %s unit in %s'%(self.__unit_type, self.__unit_zone.name))

    def get_faction(self):
        return self.__faction

    def get_unit_type(self):
        return self.__unit_type

    def set_unit_type(self, unit_type):
        self.__unit_type = unit_type

    def set_unit_gate_state(self, gate_state):
        self.__unit_gate_state = gate_state

    def get_combat_power(self):
        return self.__combat_power

    def get_cost(self):
        return self.__cost

    def set_cost(self, cost):
        self.__cost = cost

    def get_base_movement(self):
        return self.__base_movement

    def set_base_movement(self, base_movement):
        self.__base_movement = base_movement

    def get_unit_state(self):
        return self.__unit_state

    def set_unit_state(self, unit_state):
        self.__unit_state = unit_state

class Cultist(Unit):
    def __init__(self):
        pass

class Monster(Unit):
    def __init__(self):
        pass

class GreatOldOne(Unit):
    def __init__(self):
        pass











