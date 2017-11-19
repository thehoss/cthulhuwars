from enum import Enum
from .player import Player
from .playerLogic import PlayerLogic
from flags import Flags
from .blackGoat import BlackGoat

from .board import Board
from .color import TextColor, NodeColor
from .unit import Unit, UnitType, UnitState, Faction
from .zone import Zone, GateState

from weakref import WeakKeyDictionary

# primes
class SpellStates(Enum):
    ongoing = 1
    prebattle = 2
    postbattle = 3
    battle = 4
    action = 5
    movement = 6
    placement = 7
    summon = 8
    recruit = 9
    unit = 10
    affect_opponent = 11
    affect_self = 12
    neutral = 13
    used = 14
    acquired = 15
    one_use = 16

class StateDict(dict):
    def __init__(self):
        for state in SpellStates:
            self[state.name] = False

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

class Spell(object):

    def __init__(self, title, methods={}, cost=0):
        self.name = title
        self.requirements = []
        self.effects = []
        self.state = StateDict()
        self.cost = cost
        self._methods = methods

class Grimoire(object):
    def __init__(self, player=None):
        assert isinstance(player, Player)

        self._total_spells = 0
        self._spells_acquired = 0

        self._player = player
        self._board = player.board
        self._brain = player.brain
        assert isinstance(self._brain, PlayerLogic)

        self._spells = []
        self._conditions = []

    @property
    def p(self):
        return self._player

    @property
    def board(self):
        return self._board

    @property
    def brain(self):
        return self._brain

    @property
    def spells(self):
        return self._spells

    def add_condition(self, name, test):
        new_condition = {'name': name, 'test': test}
        self._conditions.append(new_condition)

    def remove_condition(self, index):
        self._conditions.remove(index)

    def test_conditions(self):
        for condition in self._conditions:
            if condition['test'](self):
                self.remove_condition(condition)
                self.acquire_spell()

    def acquire_spell(self):
        if self._spells_acquired<self._total_spells:
            self._spells_acquired += 1
            # select a new spell for acquisition
            assert isinstance(self.brain, PlayerLogic)
            self.brain.select_spell(self._spells)

        pass

    def add_spell(self, spell):
        assert isinstance(spell, Spell)
        self._spells.append(spell)
        self._total_spells += 1


########################################### END CLASS

# test conditional functions
def condition_4zones(self):
    nzones = len(self.p.occupied_zones)
    if nzones>=4:
        return True
    return False


def condition_6zones(self):
    nzones = len(self.p.occupied_zones)
    if nzones>=6:
        return True
    return False


def condition_8zones(self):
    nzones = len(self.p.occupied_zones)
    if nzones>=8:
        return True
    return False


def condition_goo(self):
    if len(self.p._goo)>0:
        return True
    return False


def condition_sharezones(self):
    shared = True
    for player in self.board.players:
        assert isinstance(player, Player)
        player_zones = player.occupied_zones
        if len(set(self.p.occupied_zones).intersection(player_zones))<=0:
            shared = False
    return shared


def condition_sacrifice(self):
    return self.p.sacrificed_two_cultists


def spell_play_thousand_young(player):
    assert isinstance(player, Player)
    pass


def spell_play_frenzy(player):
    assert isinstance(player, Player)
    for cultist in player._cultists:
        cultist.set_combat_power(1)


# test harness for grimoire class
# grim = Grimoire(BlackGoat())
# thousand_young_spell = Spell("Thousand Young", methods={"ongoing": spell_play_thousand_young}, cost=0)
# thousand_young_spell.ongoing = True
# thousand_young_spell.summon = True
# grim.add_spell(thousand_young_spell)

frenzy_spell = Spell("Frenzy", methods={"ongoing": spell_play_frenzy}, cost=0)
frenzy_spell.state.ongoing = True
frenzy_spell.state.unit = True
print(frenzy_spell.state)
# grim.add_spell(frenzy_spell)

# grim.add_condition("units in 4 zones", condition_4zones)
# grim.add_condition("units in 6 zones", condition_6zones)
# grim.add_condition("units in 8 zones", condition_8zones)
# grim.add_condition("shared zones with all opponents", condition_sharezones)
# grim.add_condition("goo summoned", condition_goo)
# grim.add_condition("sacrifice 2 cultists", condition_sacrifice)
