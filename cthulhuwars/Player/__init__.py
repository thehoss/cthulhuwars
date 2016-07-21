from core import Player
from Cthulhu import Cthulhu
from BlackGoat import BlackGoat
from YellowSign import YellowSign
from CrawlingChaos import CrawlingChaos

from cthulhuwars.Zone import Zone

#This will fail without creating the home Zone class instances first!
if __name__ == "__main__":
    south_pacific = Zone('South Pacific', isOcean=True)
    P1 = Cthulhu(south_pacific, name='Mrs. Reynolds')
    P1.player_setup()
    P1.print_state()

    africa = Zone('Africa', isOcean=False)
    P2 = BlackGoat(africa, name='Mrs. Haase')
    P2.player_setup()
    P2.print_state()

    europe = Zone('Europe', isOcean=False)
    P3 = YellowSign(europe, name='Slim Pickens')
    P3.player_setup()
    P3.print_state()

    asia = Zone('Asia', isOcean=False)
    P4 = CrawlingChaos(asia, name='Al Pacino')
    P4.player_setup()
    P4.print_state()

    # lets say it's the next turn for P2
    P2.recompute_power()
    P2.summon_dark_young(africa)
    P2.print_state()