import random

from enum import Enum

from cthulhuwars.Color import TextColor
from cthulhuwars.Maps import Map
from cthulhuwars.Player import BlackGoat
from cthulhuwars.Player import CrawlingChaos
from cthulhuwars.Player import Cthulhu
from cthulhuwars.Player import Player
from cthulhuwars.Player import YellowSign


class Actions(Enum):
    move = 0
    summon = 1
    build_gate = 2
    combat = 3
    capture = 4
    special = 5
    pass_turn = 6
    control_gate = 7
    abandon_gate = 8


class Phase(Enum):
    gather_power = 'gather power'
    first_player = 'first player'
    action = 'action'
    doom = 'doom'
    annihilation = 'annihilation'


class Board(object):
    def __init__(self):
        num_players = raw_input("Please enter the number of players:")
        self.__map = None
        self.cthulhu = False
        self.black_goat = False
        self.crawling_chaos = False
        self.yellow_sign = False
        self.__players = []
        self.__num_players = int(num_players)
        self._phase = Phase.gather_power
        self._round = 0

    @property
    def players(self):
        return self.__players

    def build_map(self):
        print(TextColor.BOLD + "Building The Map" + TextColor.ENDC)
        nplayers = self.__num_players
        map_type = [
                     'earth2Pa',
                     'earth2Pb',
                     'earth3P',
                     'earth4Pb',
                     'earth5P'
                     ]
        self.__map = Map(nplayers, map_type[nplayers-1])

    def show_map(self, image='image'):
        self.__map.show_map(image)

    def render_map(self, image='image'):
        self.__map.render_map(image)

    def create_players(self):
        assert isinstance(self.__map, Map)
        for p in range(1, int(self.__num_players) + 1):
            print('Player %s please select a faction:' % p)
            if self.cthulhu is False:
                print(TextColor.GREEN + ' [1] The Great Cthulhu' + TextColor.ENDC)
            if self.black_goat is False:
                print(TextColor.RED + ' [2] The Black Goat' + TextColor.ENDC)
            if self.crawling_chaos is False:
                print(TextColor.BLUE + ' [3] The Crawling Chaos' + TextColor.ENDC)
            if self.yellow_sign is False:
                print(TextColor.YELLOW + ' [4] The Yellow Sign' + TextColor.ENDC)
            selection = int(raw_input("Selection: "))

            if selection is 1:
                self.cthulhu = True
                self.__players.append(Cthulhu(self.__map.zone_by_name('South Pacific'),self))
            elif selection is 2:
                self.black_goat = True
                try:
                    self.__players.append(BlackGoat(self.__map.zone_by_name('Africa'), self))
                except KeyError:
                    self.__players.append(BlackGoat(self.__map.zone_by_name('West Africa'), self))
            elif selection is 3:
                self.crawling_chaos = True
                try:
                    self.__players.append(CrawlingChaos(self.__map.zone_by_name('Asia'), self))
                except KeyError:
                    self.__players.append(CrawlingChaos(self.__map.zone_by_name('South Asia'), self))
            elif selection is 4:
                self.yellow_sign = True
                self.__players.append(YellowSign(self.__map.zone_by_name('Europe'), self))

    def print_state(self):
        for p in self.__players:
            assert isinstance(p, Player)
            p.print_state()

    def start(self):
        # Returns a representation of the starting state of the game.
        for p in self.__players:
            assert isinstance(p, Player)
            p.player_setup()

    def gather_power_phase(self):
        print(TextColor.BOLD + "**Gather Power Phase **" + TextColor.ENDC)
        max_power = 0
        first_player = None
        if self.cthulhu is True:
            first_player = [player for player in self.__players if isinstance(player, Cthulhu)]

        first_player_index = 0
        for p in self.__players:
            assert isinstance(p, Player)
            p.recompute_power()

            if p.power > max_power:
                max_power = p.power
                first_player = p
            first_player_index += 1
        # shift direction can changer here
        self.__players =self.__players[first_player_index:]+self.__players[:first_player_index]

        print(TextColor.BOLD + "**First Player is %s **"%first_player._name + TextColor.ENDC)


    def tally_player_power(self):
        total_power = 0
        for p in self.__players:
            total_power += p.power
        return total_power

    def is_action_phase(self):
        if self.tally_player_power() > 0:
            return True
        else:
            return False

    def test_actions(self):

        for p in self.__players:
            assert isinstance(p, Player)
            if p.power is 0:
                print(TextColor.BOLD + "Player %s is out of power!" % p.faction.value + TextColor.ENDC)
            else:
                p.execute_action(self.__map)

    def current_player(self, state):
        # Takes the game state and returns the current player's
        # number.
        pass

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        pass

    def legal_plays(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        pass

    def winner(self, state_history):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        pass
