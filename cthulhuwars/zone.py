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
        self.desecration_state = False
        self.gate_state = GateState.noGate
        self.gate_unit  = None
        self.occupancy_list = []

    def setGateState(self, gateState):
        self.gate_state = gateState

    def setGateUnit(self, unit):
        self.gate_unit = unit

    def addUnit(self, unit):
        self.occupancy_list.append(unit)

    def removeUnit(self, unit):
        try:
            index = self.occupancy_list.index(unit)
            self.occupancy_list.pop(index)
        except ValueError:
            pass

    def setDesecrationState(self, desecrationState):
        self.desecrationState = desecrationState

    def getZoneState(self):
        zoneState = (self.gate_state, self.gate_unit, self.occupancy_list, self.desecration_state)
        return zoneState

