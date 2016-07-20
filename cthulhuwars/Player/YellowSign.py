from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState

class YellowSign(Player):
    def __init__(self, faction=Faction.yellow_sign, home_zone=Zone('Europe', False), name='The Yellow Sign'):
        super(YellowSign, self).__init__(faction, home_zone, name)
