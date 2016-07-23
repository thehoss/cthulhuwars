from enum import Enum


class TextColor():
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class NodeColor():
    BLUE = (0.2, 0.2, 0.7)
    GREEN = (0.2, 0.7, 0.2)
    YELLOW = (0.7, 0.7, 0.2)
    RED = (0.7, 0.2, 0.2)
    BLACK = (0.0, 0.0, 0.0)

