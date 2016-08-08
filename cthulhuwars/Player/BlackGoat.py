from __future__ import print_function

"""
 Black Goat faction class
 Home Zone is Africa or East Africa:
 Zone('Africa', False)
"""

# TODO: implement spell conditions
# TODO: implement Avatar ability for shub-nuggurath
# TODO: implement Fertility Cult in summoning logic
from core import Player
from cthulhuwars.Color import TextColor, NodeColor
from cthulhuwars.Unit import Unit, UnitType, UnitState, Faction
from cthulhuwars.Zone import Zone, GateState

class BlackGoat(Player):
    def __init__(self, home_zone, board, name='The Black Goat'):
        super(BlackGoat, self).__init__(Faction.black_goat, home_zone, board, name)
        '''
        Unit Lists
        The following lists are conveniences linking the relevant units from self._units
        '''
        self._dark_young = []
        self._fungi = []
        self._ghouls = []
        self._shub_niggurath = None
        '''
        Spell Book Conditions
        True = Spell Conditions have been met
        '''
        self.awakened_shub_niggurath = False
        self.units_in_four_zones = False
        self.units_in_six_zones = False
        self.units_in_eight_zones = False
        self.share_zones_with_all_factions = False
        self.sacrifice_two_cultists = False
        '''
        spell flags
        True = spell has been acquired by player
        '''
        self.spell_thousand_young = False
        self.spell_frenzy = False
        self.spell_necrophagy = False
        self.spell_ghroth = False
        self.spell_red_sign = False
        self.spell_blood_sacrifice = False
        '''
        drawing colors
        '''
        self._color = TextColor.RED
        self._node_color = NodeColor.RED
        self.probability_dict = {
            'capture': 0.3,
            'build': 0.2,
            'move': 0.3,
            'summon': 0.15,
            'recruit': 0.05,
            'combat': 0,
            'awaken': 0,
            'special': 0
        }

    @property
    def dark_young_in_play(self):
        result = 0
        for dy in self._dark_young:
            if dy.unit_state is UnitState.in_play:
                result += 1
        return result

    @property
    def fungi_in_play(self):
        result = 0
        for dy in self._fungi:
            if dy.unit_state is UnitState.in_play:
                result += 1
        return result

    @property
    def ghouls_in_play(self):
        result = 0
        for dy in self._ghouls:
            if dy.unit_state is UnitState.in_play:
                result += 1
        return result

    @property
    def goo_in_play(self):
        return self._shub_niggurath.__len__()

    def player_setup(self):
        super(BlackGoat, self).player_setup()
        n_dark_young = 3
        n_ghoul = 2
        n_fungi = 4
        for _ in range(n_dark_young):
            new_dy = DarkYoung(self, self._pool)
            self.add_unit(new_dy)
            self._dark_young.append(new_dy)

        for _ in range(n_ghoul):
            new_g = Ghoul(self, self._pool)
            self.add_unit(new_g)
            self._ghouls.append(new_g)

        for _ in range(n_fungi):
            new_f = Fungi(self, self._pool)
            self.add_unit(new_f)
            self._fungi.append(new_f)

        self._shub_niggurath = ShubNiggurath(self, self._pool)
        self.add_unit(self._shub_niggurath)
        self._goo.append(self._shub_niggurath)
        self._monsters.append(self._shub_niggurath)

    def find_build_actions(self):
        build_actions = []
        builders = self.cultists_in_play
        if self.spell_red_sign is True:
            builders = builders+self._dark_young
        if self.power >= 3:
            for cultist in builders:
                if cultist.unit_state is UnitState.in_play:
                    if cultist.gate_state is GateState.noGate and cultist.unit_zone.gate_state is GateState.noGate:
                        build_actions.append((cultist, cultist.unit_zone, None))
        return build_actions

    def capture_gate(self, unit):
        can_capture = False
        if unit.unit_type is UnitType.cultist:
            can_capture = True
        if self.spell_red_sign is True and unit.unit_type is UnitType.dark_young:
            can_capture = True

        if can_capture is True:
            if unit.gate_state is not GateState.occupied:
                if unit.unit_zone.gate_state is GateState.emptyGate:
                    unit.set_unit_gate_state(GateState.occupied)
                    unit.unit_zone.set_gate_unit(unit)
                    self._current_gates += 1
                    return True
        return False

    def summon_fungi(self, unit_zone):
        unit_cost = 2
        if self.spell_thousand_young:
            unit_cost = 1
        if self.power >= unit_cost:
            for fungi in self._fungi:
                if fungi.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(
                            self._color + TextColor.BOLD + 'A Fungi From Yuggoth has materialized!' + TextColor.ENDC)
                        fungi.set_unit_state(UnitState.in_play)
                        fungi.set_unit_zone(unit_zone)
                        return True
        return False

    def summon_ghoul(self, unit_zone):
        unit_cost = 1
        if self.spell_thousand_young:
            unit_cost = 0
        if self.power >= unit_cost:
            for ghoul in self._ghouls:
                if ghoul.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + TextColor.BOLD + 'A Ghoul appears!' + TextColor.ENDC)
                        ghoul.set_unit_state(UnitState.in_play)
                        ghoul.set_unit_zone(unit_zone)
                        return True
        return False

    def summon_dark_young(self, unit_zone):
        unit_cost = 3
        if self.spell_thousand_young:
            unit_cost = 2
        if self.power >= unit_cost:
            for dark_young in self._dark_young:
                if dark_young.unit_state is UnitState.in_reserve:
                    if self.spend_power(unit_cost):
                        print(self._color + TextColor.BOLD + 'A Dark Young has been summoned!' + TextColor.ENDC)
                        dark_young.set_unit_state(UnitState.in_play)
                        dark_young.set_unit_zone(unit_zone)
                        return True
        return False

    def summon_shub_niggurath(self, unit_zone):
        assert isinstance(unit_zone, Zone)
        unit_cost = 8
        # Do we have enough power?
        if self.power >= unit_cost:
            print(
                self._color + TextColor.BOLD + 'The Black Goat is attempting to awaken Shub-Niggurath!' + TextColor.ENDC)
            # is there a gate in the summoning zone, and do we occupy it?
            if unit_zone.gate_state is GateState.occupied:
                if unit_zone.gate_unit.faction == self:
                    # make sure we have enough cultists to sacrifice.
                    # Per Errata: must have controlled gate and two cultists anywhere
                    # interact with user to determine which cultists to sacrifice
                    # assumes gate occupying cultists will not be sacrificed
                    cultists = self.cultists_in_play
                    if len(cultists) >= 2:
                        for i in range(2):
                            kill_list = []
                            for c in cultists:
                                # TODO: remove occupancy assumption, replace with logic
                                # if unit.gate_state is not GateState.occupied:
                                kill_list.append(c)
                            # Uncomment below to allow user selection of cultists to sacrifice
                            '''
                            print(self._color + 'Pick a cultist to sacrifice:')
                            for n in range(len(kill_list)):
                                print('  [' + str(n) + '] Cultist in %s' % kill_list[n].unit_zone.name)
                            while True:
                                sacrifice = int(raw_input('Selection:'))
                                if sacrifice < len(kill_list):
                                    break
                            '''
                            self.remove_unit(kill_list[i])
                        # put shub_niggurath on the board, and spend the power
                        self._shub_niggurath.set_unit_zone(unit_zone)
                        self._shub_niggurath.set_unit_state(UnitState.in_play)
                        self.spend_power(unit_cost)
                        if not self.awakened_shub_niggurath:
                            self.take_new_spell()
                        print(
                            self._color + TextColor.BOLD + 'Shub-Niggurath Successfully Summoned!' + TextColor.ENDC)
                        return True
        return False

    def spell_play_thousand_young(self):
        self.spell_thousand_young = True

    def spell_play_red_sign(self):
        self.spell_red_sign = True

    def spell_play_frenzy(self):
        self.spell_frenzy = True
        for cultist in self._cultists:
            cultist.set_combat_power(1)

    def spell_play_ghroth(self):
        self.spell_ghroth = True

    def spell_play_necrophagy(self):
        self.spell_necrophagy = True

    def take_new_spell(self):
        # check conditions for taking a new spell:
        # Have Units in four Areas
        # Have Units in six Areas
        # Have Units in eight Areas
        # As your Action for a Round, eliminate two of your Cultists
        # Share Areas with all enemies (i.e. both you and your enemy have Units there.)
        # Awaken Shub-Niggurath
        nzones = len(self.occupied_zones)
        if nzones >= 4 and self.units_in_four_zones is False:
            self.units_in_four_zones = True
            # pick a spell
        if nzones >= 6 and self.units_in_six_zones is False:
            self.units_in_six_zones = True
            # pick a spell
        if nzones >= 8 and self.units_in_eight_zones is False:
            self.units_in_eight_zones = True
            # pick a spell
        if self._shub_niggurath is not None and self.awakened_shub_niggurath is False:
            self.awakened_shub_niggurath = True
            # pick a spell
        # check for shared areas condition
        if self.share_zones_with_all_factions is False:
            shared = True
            for player in self._board.players:
                assert isinstance(player, Player)
                player_zones = player.occupied_zones
                if len(set(self._occupied_zones).intersection(player_zones)) <= 0:
                    shared = False
            if shared is True:
                self.share_zones_with_all_factions = True
                # Pick a spell

        pass

    def sacrifice_two_cultists(self):
        candidates = []
        for cultist in self._cultists:
            assert isinstance(cultist, Unit)
            if cultist.unit_state is UnitState.in_play:
                if cultist.gate_state is GateState.noGate:
                    candidates.append(cultist)

        if candidates.__len__() >= 2:
            # Kills off the first two found
            # TODO: figure out least valuable cultists in candidate list and sacrifice them
            for n in range(0, 2):
                self.kill_unit(candidates[n])
            self.sacrifice_two_cultists = True
            # Pick a Spell
            return True
        else:
            return False

    def summon_action(self, monster, unit_zone):
        assert isinstance(monster, Unit)
        if monster.unit_state is UnitState.in_reserve:
            if monster.unit_type is UnitType.dark_young:
                return self.summon_dark_young(unit_zone)
            if monster.unit_type is UnitType.fungi:
                return self.summon_fungi(unit_zone)
            if monster.unit_type is UnitType.ghoul:
                return self.summon_ghoul(unit_zone)
            if monster.unit_type is UnitType.shub_niggurath:
                return self.summon_shub_niggurath(unit_zone)
        return False

    def recompute_power(self):
        super(BlackGoat, self).recompute_power()
        if self.spell_red_sign:
            self._power += self.dark_young_in_play


class Ghoul(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(Ghoul, self).__init__(unit_parent, unit_zone, UnitType.ghoul, combat_power=0, cost=unit_cost,
                                    base_movement=1,
                                    unit_state=UnitState.in_reserve)

    def render_unit(self):
        render_definition = {
            "nodetype": ["sphere"],
            "name": ["%s_%s" % (self.faction._name, self._unit_type.value)],
            "params": [("float", "radius", 0.025)]
        }
        return render_definition


class Fungi(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(Fungi, self).__init__(unit_parent, unit_zone, UnitType.fungi, combat_power=1, cost=unit_cost,
                                    base_movement=1,
                                    unit_state=UnitState.in_reserve)

    def render_unit(self):
        render_definition = {
            "nodetype": ["sphere"],
            "name": ["%s_%s" % (self.faction._name, self._unit_type.value)],
            "params": [("float", "radius", 0.03)]
        }
        return render_definition


class DarkYoung(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=0):
        super(DarkYoung, self).__init__(unit_parent, unit_zone, UnitType.dark_young, combat_power=2, cost=unit_cost,
                                        base_movement=1,
                                        unit_state=UnitState.in_reserve)

    def render_unit(self):
        render_definition = {
            "nodetype": ["sphere"],
            "name": ["%s_%s" % (self.faction._name, self._unit_type.value)],
            "params": [("float", "radius", 0.035)]
        }
        return render_definition


class ShubNiggurath(Unit):
    def __init__(self, unit_parent, unit_zone, unit_cost=8):
        super(ShubNiggurath, self).__init__(unit_parent, unit_zone, UnitType.shub_niggurath, combat_power=0, cost=unit_cost,
                                            base_movement=1,
                                            unit_state=UnitState.in_reserve)

    @property
    def combat_power(self):
        total_combat_power = self.faction.current_cultists + self.faction.current_gates
        if self.faction.spell_red_sign:
            total_combat_power += self.faction.dark_young_in_play
        return total_combat_power

    def render_unit(self):
        render_definition = {
            "nodetype": ["sphere"],
            "name": ["%s_%s" % (self.faction._name, self._unit_type.value)],
            "params": [("float", "radius", 0.085)]
        }
        return render_definition
