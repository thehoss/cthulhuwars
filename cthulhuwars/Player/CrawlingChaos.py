from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState

#  Crawling Chaos
#  Starts in Asia or East Asia
#

class CrawlingChaos(Player):
    def __init__(self, home_zone, name='The Crawling Chaos'):
        super(CrawlingChaos, self).__init__(Faction.crawling_chaos, home_zone, name)
