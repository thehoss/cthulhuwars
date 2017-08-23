"""
cthulhuWars
Zone Class
Instances of the Zone class contain zone description and prior state

TODO:

"""

from enum import Enum
from .color import NodeColor

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
        self.occupancy_list = set()
        self.color = NodeColor.BLACK

        # these values are set at map construction and do not change
        # (however, they would change on the Primeval map and Shaggai
        #  because zones are effectively removed from the board during gameplay)
        self.closeness_centrality = 0.0
        self.betweenness_centrality = 0.0
        self.eigenvector_centrality = 0.0

        # two buffers as dicts of lists containing faction influence values
        self.faction_influence_dictA = dict()
        self.faction_influence_dictB = dict()

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
        self.occupancy_list.add(unit)
        #unit.set_unit_zone(self)

    def remove_unit(self, unit):
        try:
            #index = self.occupancy_list.index(unit)
            #self.occupancy_list.pop(index)
            self.occupancy_list.discard(unit)
        except ValueError:
            pass

    def set_betweenness_centrality(self, value):
        self.betweenness_centrality = value

    def set_closeness_centrality(self, value):
        self.closeness_centrality = value

    def set_eigenvector_centrality(self, value):
        self.eigenvector_centrality = value

    # influence uses two buffers to compute
    # result is read from buffer A
    def reset_influence(self, faction):
        try:
            self.faction_influence_dictA[faction].clear()
            self.faction_influence_dictB[faction].clear()
        except KeyError:
            pass

    def set_influenceA(self, faction, type, value):
        # set influence value for influence type
        type_value = {type: value}
        self.faction_influence_dictA[faction] = type_value

    def set_influenceB(self, faction, type, value):
        # set influence value for influence type
        type_value = {type: value}
        self.faction_influence_dictB[faction] = type_value

    def get_influenceA(self, faction, type):
        return self.faction_influence_dictA[faction][type]

    def get_influenceB(self, faction, type):
        return self.faction_influence_dictB[faction][type]

    def get_influence(self, faction, type):
        return self.faction_influence_dictA[faction][type]

    def copy_to_influenceA(self):
        self.faction_influence_dictA = self.faction_influence_dictB

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

