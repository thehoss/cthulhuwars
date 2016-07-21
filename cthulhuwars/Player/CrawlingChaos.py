from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState

#  Crawling Chaos
#  Starts in Asia or East Asia
#
class text_colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CrawlingChaos(Player):
    def __init__(self, home_zone, name='The Crawling Chaos'):
        super(CrawlingChaos, self).__init__(Faction.crawling_chaos, home_zone, name)
        self.__color = text_colors.BLUE

    def print_state(self):
        print (self.__color)
        super(CrawlingChaos,self).print_state()
