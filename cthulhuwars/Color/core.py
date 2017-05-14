from enum import Enum

class TextColor():
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    FactionColor = {
        'cthulhu': GREEN,
        'black_goat': RED,
        'crawling_chaos': BLUE,
        'yellow_sign': YELLOW
    }


class NodeColor():
    BLUE = (0.5, 0.5, 0.75)
    GREEN = (0.5, 0.75, 0.5)
    YELLOW = (0.75, 0.75, 0.5)
    RED = (0.75, 0.5, 0.5)
    BLACK = (0.0, 0.0, 0.0)

    FactionColor = {
        'cthulhu': GREEN,
        'black_goat': RED,
        'crawling_chaos': BLUE,
        'yellow_sign': YELLOW
    }


class NodeColorINT():
    BLUE = (122, 122, 235)
    GREEN = (122, 235, 122)
    YELLOW = (235, 235, 122)
    RED = (235, 122, 122)
    BLACK = (0, 0, 0)

    FactionColor = {
        'cthulhu': GREEN,
        'black_goat': RED,
        'crawling_chaos': BLUE,
        'yellow_sign': YELLOW
    }