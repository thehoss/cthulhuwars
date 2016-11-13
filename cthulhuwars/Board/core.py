import random

from enum import Enum

from cthulhuwars.Color import TextColor
from cthulhuwars.Maps import Map
from cthulhuwars.Player import Player, BlackGoat, CrawlingChaos, Cthulhu, YellowSign

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
        num_players = 4

        self.__map = None

        self.cthulhu = False
        self._cthulhu = None

        self.black_goat = False
        self._black_goat = None

        self.crawling_chaos = False
        self._crawling_chaos = None

        self.yellow_sign = False
        self._yellow_sign = None

        self.__players = []

        self.player_dict = {
            'cthulhu': {'active':False, 'class': None, 'address': [], 'turn': 0} ,
            'black_goat': {'active': False, 'class': None, 'address': [], 'turn': 1},
            'crawling_chaos': {'active': False, 'class': None, 'address': [], 'turn': 2},
            'yellow_sign': {'active': False, 'class': None, 'address': [], 'turn': 3}
        }

        self.__num_players = int(num_players)
        self._phase = Phase.gather_power
        self._round = 0
        self._doom_track = {}

    @property
    def players(self):
        return self.__players

    @property
    def map(self):
        return self.__map

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

    def create_all_players(self):
        assert isinstance(self.__map, Map)

        index = self.__players.__len__()
        self.player_dict['cthulhu']['class'] = Cthulhu(self.__map.zone_by_name('South Pacific'),self)
        self.__players.append(self.player_dict['cthulhu']['class'])

        try:
            self.player_dict['black_goat']['class'] = BlackGoat(self.__map.zone_by_name('Africa'), self)
            self.__players.append(self.player_dict['black_goat']['class'])
        except KeyError:
            self.player_dict['black_goat']['class'] = BlackGoat(self.__map.zone_by_name('West Africa'), self)
            self.__players.append(self.player_dict['black_goat']['class'])

        try:
            self.player_dict['crawling_chaos']['class'] = CrawlingChaos(self.__map.zone_by_name('Asia'), self)
            self.__players.append(self.player_dict['crawling_chaos']['class'])
        except KeyError:
            self.player_dict['crawling_chaos']['class'] = CrawlingChaos(self.__map.zone_by_name('South Asia'), self)
            self.__players.append(self.player_dict['crawling_chaos']['class'])

        self.player_dict['yellow_sign']['class'] = YellowSign(self.__map.zone_by_name('Europe'), self)
        self.__players.append(self.player_dict['yellow_sign']['class'])

        for p in self.__players:
            assert isinstance(p, Player)
            self._doom_track[p._name] = 0

    def create_players(self):
        assert isinstance(self.__map, Map)
        index = 0
        for p in range(1, int(self.__num_players) + 1):
            # print('Player %s please select a faction:' % p)
            print ('Please the select the factions that will be in play...')
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
                self.player_dict['cthulhu']['active'] = True
                index = self.__players.__len__()
                self.__players.append(Cthulhu(self.__map.zone_by_name('South Pacific'),self))
            elif selection is 2:
                self.black_goat = True
                self.player_dict['black_goat']['active'] = True
                try:
                    self.__players.append(BlackGoat(self.__map.zone_by_name('Africa'), self))
                except KeyError:
                    self.__players.append(BlackGoat(self.__map.zone_by_name('West Africa'), self))
            elif selection is 3:
                self.player_dict['crawling_chaos']['active'] = True
                self.crawling_chaos = True
                try:
                    self.__players.append(CrawlingChaos(self.__map.zone_by_name('Asia'), self))
                except KeyError:
                    self.__players.append(CrawlingChaos(self.__map.zone_by_name('South Asia'), self))
            elif selection is 4:
                self.player_dict['yellow_sign']['active'] = True
                self.yellow_sign = True
                self.__players.append(YellowSign(self.__map.zone_by_name('Europe'), self))

        for p in self.__players:
            assert isinstance(p, Player)
            self._doom_track[p._name] = 0


    def print_state(self):
        for p in self.__players:
            assert isinstance(p, Player)
            p.print_state()

    def start(self):
        # Returns a representation of the starting state of the game.
        # Rule:  If present, The Great Cthulhu goes first on first turn
        cIndex = 0
        print ('Game Starting: Generating random player turn order...')
        if self.player_dict['cthulhu']['active']:
            print ('The Great Cthulhu faction holds primacy for the first turn!')
            self.cthulhu = True
            cthulhu = self.__players.pop(cIndex)
            random.shuffle(self.__players)
            self.__players.insert(0, cthulhu)
        else:
            random.shuffle(self.__players)
        t = 0
        for p in self.__players:
            assert isinstance(p, Player)
            self.player_dict[p.short_name]['turn'] = t
            t += 1
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

    def doom_phase(self):
        max_doom = 0
        win_condition = 30
        lead = ''
        for p in self.__players:
            assert isinstance(p, Player)
            self._doom_track[p._name] += p.doom_points
            if self._doom_track[p._name] > max_doom:
                max_doom = self._doom_track[p._name]
                lead = p._name

        print self._doom_track

        if self._doom_track[lead] > win_condition:
            print(TextColor.BOLD + "**%s Wins! **" % lead + TextColor.ENDC)
            return True
        else:
            return False


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
            self.pre_turn_actions()
            if p.power is 0:
                print(TextColor.BOLD + "Player %s is out of power!" % p.faction.value + TextColor.ENDC)
            else:
                p.brain.execute_action()
            self.post_turn_actions()


    def post_combat_actions(self):
        for p in self.__players:
            assert isinstance(p, Player)
            p.post_combat_action()

    def pre_turn_actions(self):
        for p in self.__players:
            assert isinstance(p, Player)
            p.pre_turn_action()

    def post_turn_actions(self):
        for p in self.__players:
            assert isinstance(p, Player)
            p.post_turn_action()

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
