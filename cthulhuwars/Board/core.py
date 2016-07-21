from cthulhuwars.Maps import Map
from cthulhuwars.Player import BlackGoat,CrawlingChaos,Cthulhu,YellowSign,Player

class text_colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Board(object):

    def __init__(self):
        num_players = raw_input("Please enter the number of players:")
        self.__map = None
        self.cthulhu = False
        self.black_goat = False
        self.crawling_chaos = False
        self.yellow_sign = False
        self.__players = []
        self.__num_players = num_players

    def build_map(self):
        print(text_colors.BOLD+"Building The Map"+text_colors.ENDC)
        self.__map = Map(self.__num_players, 'earth4Pa')

    def create_players(self):
        assert isinstance(self.__map, Map)
        for p in range(1, int(self.__num_players)+1):
            print('Player %s please select a faction:'%p)
            if self.cthulhu is False:
                print(text_colors.GREEN + ' [1] The Great Cthulhu' + text_colors.ENDC)
            if self.black_goat is False:
                print(text_colors.RED + ' [2] The Black Goat' + text_colors.ENDC)
            if self.crawling_chaos is False:
                print(text_colors.BLUE + ' [3] The Crawling Chaos' + text_colors.ENDC)
            if self.yellow_sign is False:
                print(text_colors.YELLOW + ' [4] The Yellow Sign' + text_colors.ENDC)
            selection = int(raw_input("Selection: "))

            if selection is 1:
                self.cthulhu = True
                self.__players.append(Cthulhu(self.__map.zone_by_name('South Pacific')))
            elif selection is 2:
                self.black_goat = True
                self.__players.append(BlackGoat(self.__map.zone_by_name('Africa')))
            elif selection is 3:
                self.crawling_chaos = True
                self.__players.append(CrawlingChaos(self.__map.zone_by_name('Asia')))
            elif selection is 4:
                self.yellow_sign = True
                self.__players.append(YellowSign(self.__map.zone_by_name('Europe')))

    def print_state(self):
        for p in self.__players:
            assert isinstance(p, Player)
            p.print_state()

    def start(self):
        # Returns a representation of the starting state of the game.
        for p in self.__players:
            assert isinstance(p, Player)
            p.player_setup()
        self.print_state()


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


