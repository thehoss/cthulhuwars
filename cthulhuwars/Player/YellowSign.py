from core import Player
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState
from cthulhuwars.Color import TextColor, NodeColor

# Yellow Sign
# Starts in Europe


class YellowSign(Player):
    def __init__(self, home_zone, board, name='The Yellow Sign'):
        super(YellowSign, self).__init__(Faction.yellow_sign, home_zone, board, name)
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


class Undead(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost):
        super(Undead, self).__init__(unit_parent, unit_zone, UnitType.undead, combat_power=None, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)
class Byakhee(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost):
        super(Byakhee, self).__init__(unit_parent, unit_zone, UnitType.byakhee, combat_power=None, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)
