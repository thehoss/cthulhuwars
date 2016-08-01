from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState
from cthulhuwars.Color import TextColor, NodeColor


# Yellow Sign
# Starts in Europe

class YellowSign(Player):
    def __init__(self, home_zone, board, name='The Yellow Sign'):
        super(YellowSign, self).__init__(Faction.yellow_sign, home_zone, board, name)
        self._undead = []
        self._byakhee = []
        self._hastur = None
        self._king_in_yellow = None

        self._undead_in_play = 0
        self._byakhee_in_play = 0
        self._king_in_yellow_in_play = 0
        self._hastur_in_play = 0
        self._spell_the_third_eye = False
        self._spell_he_who_is_not_to_be_named = False
        self._spell_shriek_of_the_byakhee = False
        self._spell_zingaya = False
        self._spell_passion = False
        self._spell_the_screaming_dead = False
        self._color = TextColor.YELLOW

        self._node_color = NodeColor.YELLOW

    def player_setup(self):
        super(YellowSign, self).player_setup()
        n_undead = 6
        n_byakhee = 4

        for _ in range(n_undead):
            new_u = Undead(self, self._pool)
            self.add_unit(new_u)
            self._undead.append(new_u)

        for _ in range(n_byakhee):
            new_b = Byakhee(self, self._pool)
            self.add_unit(new_b)
            self._byakhee.append(new_b)

        self._hastur = Hastur(self, self._pool)
        self.add_unit(self._hastur)
        self._goo.append(self._hastur)
        self._monsters.append(self._hastur)

        self._king_in_yellow = KingInYellow(self, self._pool)
        self.add_unit(self._king_in_yellow)
        self._goo.append(self._king_in_yellow)
        self._monsters.append(self._king_in_yellow)

class Undead(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=1):
        super(Undead, self).__init__(unit_parent, unit_zone, UnitType.undead, combat_power=None, cost=unit_cost,
                                     base_movement=1,
                                     unit_state=UnitState.in_reserve)

    @property
    def combat_power(self):
        total = -1
        for unit in self.unit_zone.occupancy_list:
            if unit.unit_type is UnitType.undead:
                total += 1
        return total

class Byakhee(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=2):
        super(Byakhee, self).__init__(unit_parent, unit_zone, UnitType.byakhee, combat_power=None, cost=unit_cost,
                                      base_movement=1,
                                      unit_state=UnitState.in_reserve)
    @property
    def combat_power(self):
        total = 1
        for unit in self.unit_zone.occupancy_list:
            if unit.unit_type is UnitType.byakhee:
                total += 1
        return total


class Hastur(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=10):
        super(Hastur, self).__init__(unit_parent, unit_zone, UnitType.hastur, combat_power=None, cost=unit_cost,
                                      base_movement=1,
                                      unit_state=UnitState.in_reserve)
    @property
    def combat_power(self):
        return 5

    def render_unit(self):
        render_definition = {
            "nodetype": ["sphere"],
            "name": ["%s_%s" % (self.faction._name, self._unit_type.value)],
            "params": [("float", "radius", 0.085)]
        }
        return render_definition


class KingInYellow(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=4):
        super(KingInYellow, self).__init__(unit_parent, unit_zone, UnitType.king_in_yellow, combat_power=None,
                                      cost=unit_cost,
                                      base_movement=1,
                                      unit_state=UnitState.in_reserve)


    def render_unit(self):
        render_definition = {
            "nodetype": ["sphere"],
            "name": ["%s_%s" % (self.faction._name, self._unit_type.value)],
            "params": [("float", "radius", 0.055)]
        }
        return render_definition
