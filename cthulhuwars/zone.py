"""
cthulhuWars
Zone Class
Instances of the Zone class contain zone description and prior state

TODO:

"""

from enum import Enum

class GateState(Enum):
    noGate    = 0
    emptyGate = 1
    occupied  = 2

class Zone:

    def __init__(self, name = 'unnamed', isOcean = False):
        self.name = name
        self.is_ocean = isOcean
        self.gate_state = GateState.noGate
        self.gate_unit  = None
        self.occupancy_list = []

    def set_gate_state(self, gateState):
        self.gate_state = gateState

    def set_gate_unit(self, unit):
        self.gate_unit = unit

    def add_unit(self, unit):
        self.occupancy_list.append(unit)

    def remove_unit(self, unit):
        try:
            index = self.occupancy_list.index(unit)
            self.occupancy_list.pop(index)
        except ValueError:
            pass

    def get_zone_state(self):
        zoneState = (self.gate_state, self.gate_unit, self.occupancy_list)
        return zoneState

