from enum import Enum
from .player import Player
from .playerLogic import PlayerLogic

from .board import Board
from .color import TextColor, NodeColor
from .unit import Unit, UnitType, UnitState, Faction
from .zone import Zone, GateState


class Spell(object):
    def __init__(self, name, method=[], cost=0):
        self.name = name
        self.requirements = []
        self.effects = []
        self._status = {"ongoing": False, "prebattle": False, "postbattle": False, "action": False, "movement": False,
                        "placement": False, "summon": False, "recruit": False,
                        "affect_opponent": False, "affect_self": False, "neutral": False, "used": False,
                        "one_use": False,
                        'acquired': False}
        self.cost = cost
        self.method = method

    @property
    def ongoing(self):
        return self._status["ongoing"]

    @ongoing.setter
    def ongoing(self, v):
        self._status["ongoing"] = v

    @property
    def one_use(self):
        return self._status["one_use"]

    @one_use.setter
    def one_use(self, v):
        self._status["one_use"] = v

    @property
    def usable(self):
        if (self._status["one_use"] & self._status["used"]):
            return False
        return True

    @usable.setter
    def usable(self, v):
        self._status["usable"] = v

    @property
    def acquired(self):
        return self._status["acquired"]

    @acquired.setter
    def acquired(self, v):
        self._status["acquired"] = v

    @property
    def affect_self(self):
        return self._status["affect_self"]

    @affect_self.setter
    def affect_self(self, v):
        self._status["affect_self"] = v

    @property
    def affect_opponent(self):
        return self._status["affect_opponent"]

    @affect_opponent.setter
    def affect_opponent(self, v):
        self._status["affect_opponent"] = v

    @property
    def prebattle(self):
        return self._status["prebattle"]

    @prebattle.setter
    def prebattle(self, v):
        self._status["prebattle"] = v

    @property
    def postbattle(self):
        return self._status["postbattle"]

    @postbattle.setter
    def postbattle(self, v):
        self._status["postbattle"] = v

    @property
    def summon(self):
        return self._status["summon"]

    @summon.setter
    def summon(self, v):
        self._status["summon"] = v

    @property
    def action(self):
        return self._status["action"]

    @action.setter
    def action(self, v):
        self._status["action"] = v

    @property
    def movement(self):
        return self._status["movement"]

    @movement.setter
    def movement(self, v):
        self._status["movement"] = v

    @property
    def placement(self):
        return self._status["placement"]

    @placement.setter
    def placement(self, v):
        self._status["placement"] = v

    def set_status(self, key, value):
        self._status[key] = value


class Grimoire(object):
    def __init__(self, player):
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
    if nzones >= 4:
        return True
    return False


def condition_6zones(self):
    nzones = len(self.p.occupied_zones)
    if nzones >= 6:
        return True
    return False


def condition_8zones(self):
    nzones = len(self.p.occupied_zones)
    if nzones >= 8:
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


# test harness for grimoire class
def __test__():
    grim = Grimoire(Player())
    thousand_young_spell = Spell("Thousand Young", method=[spell_play_thousand_young], cost=0)
    thousand_young_spell.ongoing = True
    thousand_young_spell.summon = True
    grim.add_spell(thousand_young_spell)

    grim.add_condition("units in 4 zones", condition_4zones)
    grim.add_condition("units in 6 zones", condition_6zones)
    grim.add_condition("units in 8 zones", condition_8zones)
    grim.add_condition("shared zones with all opponents", condition_sharezones)
    grim.add_condition("goo summoned", condition_goo)
    grim.add_condition("sacrifice 2 cultists", condition_sacrifice)
