from .player import Player
from .board import Board
from .color import TextColor, NodeColor
from .unit import Unit, UnitType, UnitState, Faction
from .zone import Zone, GateState

class Spell(object):
    def __init__(self, name):
        self.name = name
        self.requirements = []
        self.effects = []

class Grimoire(object):
    def __init__(self, player):
        assert isinstance(player, Player)

        self._total_spells = 6
        self._spells_acquired = 0

        self._player = player
        self._board = player._board
        self._brain = player.brain
        self.spellbooks = []
        self.conditions = []

    @property
    def p(self):
        return self._player

    @property
    def b(self):
        return self._board

    def test_condition_a(self):
        nzones = len(self.p.occupied_zones)
        if nzones>=4:
            return True
        return False

    def test_condition_b(self):
        nzones = len(self.p.occupied_zones)
        if nzones>=6:
            return True
        return False

    def test_condition_c(self):
        nzones = len(self.p.occupied_zones)
        if nzones>=8:
            return True
        return False

    def test_condition_d(self):
        if len(self.p._goo) > 0:
            return True
        return False

    def test_condition_e(self):
        shared = True
        for player in self.b.players:
            assert isinstance(player, Player)
            player_zones = player.occupied_zones
            if len(set(self.p.occupied_zones).intersection(player_zones)) <= 0:
                shared = False
        return shared

    def test_condition_f(self):
        return self.p.sacrificed_two_cultists

    def addCondition(self, name, test):
        new_condition = {'name': name, 'test': test}
        self.conditions.append(new_condition)

    def remove_condition(self, index):
        self.conditions.remove(index)

    def test_conditions(self):
        for condition in self.conditions:
            if condition['test']():
                self.remove_condition(condition)
                self.acquire_spell()

    def acquire_spell(self):
        if self._spells_acquired < self._total_spells:
            self._spells_acquired += 1

        pass
