from enum import Enum

class UnitType(Enum):
    cultist = 0
    monsterA = 1
    monsterB = 2
    monsterC = 3
    GOO = 4

class Faction(Enum):
    cthulhu = 0
    black_goat = 1
    crawling_chaos = 2
    yellow_sign = 3
    sleeper = 4
    windwalker = 5
    opener_of_the_way = 6
    tcho_tcho = 7
    azathoth = 8

class UnitState(Enum):
    in_reserve = 0
    in_play    = 1
    killed     = 2
    captured   = 3


class Unit:
    def __init__(self, faction=Faction.cthulhu, unit_type=UnitType.cultist, combat_power=0, cost=1,  base_movement=1,  unit_state=UnitState.in_reserve):
        self.__faction = faction
        self.__unit_type = unit_type
        self.__combat_power = combat_power
        self.__cost = cost
        self.__base_movement = base_movement
        self.__unit_state = unit_state

    def get_faction(self):
        return self.__faction

    def get_unit_type(self):
        return self.__unit_type

    def set_unit_type(self, unit_type):
        self.__unit_type = unit_type

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













