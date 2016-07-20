from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState

class CrawlingChaos(Player):
    def __init__(self, faction=Faction.crawling_chaos, home_zone=Zone('Asia', False), name='The Crawling Chaos'):
        super(CrawlingChaos, self).__init__(faction, home_zone, name)
