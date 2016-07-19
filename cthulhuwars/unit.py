from enum import Enum

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
    def __init__(self, faction=Faction.cthulhu, combat_power=0, cost=1,  base_movement=1,
                 unit_state=UnitState.in_reserve):
        self._faction = faction
        self._combat_power = combat_power
        self._cost = cost
        self._base_movement = base_movement
        self._unit_state = unit_state

    def get_faction(self):
        return self._faction

    def get_combat_power(self):
        return self._combat_power

    def get_cost(self):
        return self._cost

    def set_cost(self, cost):
        self._cost = cost

    def get_base_movement(self):
        return self._base_movement

    def set_base_movement(self, base_movement):
        self._base_movement = base_movement

    def get_unit_state(self):
        return self._unit_state

    def set_unit_state(self, unit_state):
        self._unit_state = unit_state


class Cultist(Unit):
    def __init__(self):
        pass

class Monster(Unit):
    def __init__(self):
        pass

class GreatOldOne(Unit):
    def __init__(self):
        pass


















