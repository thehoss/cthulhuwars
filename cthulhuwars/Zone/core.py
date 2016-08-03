"""
cthulhuWars
Zone Class
Instances of the Zone class contain zone description and prior state

TODO:

"""

from enum import Enum
from cthulhuwars.Color import NodeColor

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
        self.color = NodeColor.BLACK

    def set_gate_state(self, gateState):
        self.gate_state = gateState

    def clear_gate_state(self):
        if self.gate_state is GateState.occupied:
            self.gate_state = GateState.emptyGate
            self.gate_unit = None

    def set_gate_unit(self, unit):
        self.set_gate_state(GateState.occupied)
        self.gate_unit = unit

    def add_unit(self, unit):
        self.occupancy_list.append(unit)
        #unit.set_unit_zone(self)

    def remove_unit(self, unit):
        try:
            index = self.occupancy_list.index(unit)
            self.occupancy_list.pop(index)
        except ValueError:
            pass

    def compute_color(self):
        col = (0,0,0)
        n = self.occupancy_list.__len__()
        if n > 0:
            for unit in self.occupancy_list:
                unit_color = unit.faction._node_color
                col = (col[0]+unit_color[0], col[1]+unit_color[1], col[2]+unit_color[2])
            col = (col[0]/n, col[1]/n, col[2]/n)
        return col


    def get_zone_state(self):
        zoneState = (self.gate_state, self.gate_unit, self.occupancy_list)
        return zoneState

