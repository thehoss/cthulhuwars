from enum import Enum
from .map import Map
from .unit import Unit, UnitState, UnitType
from numpy.random import choice
from .color import TextColor

class Methods(Enum):
    random = 0
    weighted_choice = 1


def clamp(n, smallest, largest): return max(smallest, min(n, largest))


class PlayerLogic(object):
    def __init__(self, player, the_map):
        assert isinstance(the_map, Map)

        self.player = player
        self._method = Methods.random
        self.map = the_map

        self._spells = []

        self._probability_dict = {
            'capture': 3.0,
            'build': 4.0,
            'move': 2.0,
            'summon': 1.0,
            'recruit': 1.0,
            'combat': 5.5,
            'awaken': 0.0,
            'special': 0.0
        }

    def use_method_random(self):
        self._method = Methods.random

    def use_method_wc(self):
        self._method = Methods.weighted_choice

    def set_probabilities(self, dict):
        self._probability_dict = dict

    def set_spells(self, spells):
        self._spells = spells

    '''
    execute_action
    collects all possible actions based on the current map and player state
    uses a weighted random choice based on the probability_dict to decide what action
     to take
     Once an action is decided on, the first action in the list is taken

     TODO: make this more robust by evaluating each action and it's short term benefits
     e.g. a move to an empty zone will be more desirable for a cultist than an occupied zone
     a move to a zone with one cultist and a gate will be very desirable for a monster

     TODO: account for battle and awaken actions
    '''

    def execute_action(self):
        result = False
        self.player.take_spell_book()

        if self._method is Methods.random:
            result = self.random_action()
        if self._method is Methods.weighted_choice:
            result = self.weighted_choice_action()
        return result

    def random_action(self):
        possible_builds = self.player.find_build_actions()
        possible_moves = self.player.find_move_actions(self.map)
        possible_captures = self.player.find_capture_actions()
        possible_summons = self.player.find_summon_actions()
        possible_recruits = self.player.find_recruit_actions()
        possible_combat = self.player.find_combat_actions()

        action_func = {
            'capture': [],
            'build': [],
            'move': [],
            'summon': [],
            'recruit': [],
            'combat': [],
            'awaken': [],
            'special': []
        }

        action_probability = {}

        if len(possible_captures) > 0:
            action_probability['capture'] = []
            action_probability['capture'].append(self._probability_dict['capture'])
            action_func['capture'] = possible_captures

        if len(possible_summons) > 0:
            action_probability['summon'] = []
            action_probability['summon'].append(self._probability_dict['summon'])
            action_func['summon'] = possible_summons

        if len(possible_moves) > 0:
            action_probability['move'] = []
            action_probability['move'].append(self._probability_dict['move'])
            action_func['move'] = possible_moves

        if len(possible_builds) > 0:
            action_probability['build'] = []
            action_probability['build'].append(self._probability_dict['build'])
            action_func['build'] = possible_builds

        if len(possible_recruits) > 0:
            action_probability['recruit'] = []
            action_probability['recruit'].append(self._probability_dict['recruit'])
            action_func['recruit'] = possible_recruits

        if len(possible_combat) > 0:
            action_probability['combat'] = []
            action_probability['combat'].append(self._probability_dict['combat'])
            action_func['combat'] = possible_combat

        action_success = False
        while action_success is False:
            if len(action_probability) > 0:
                key_list = []

                for k, v in action_probability.iteritems():
                    key_list.append(k)

                action = choice(range(len(key_list)), 1)[0]

                action_choice = choice(range(len(action_func[key_list[action]])), 1)[0]
                action_params = action_func[key_list[action]][action_choice]

                action_func.pop(key_list[action])
                action_probability.pop(key_list[action])

                if key_list[action] is 'capture':
                    action_success = self.player.capture_unit(action_params[0], action_params[1], action_params[2])

                if key_list[action] is 'move':
                    # TODO:  allow multiple moves
                    action_success = self.player.move_action(action_params[0], action_params[1],
                                                             action_params[2])

                if key_list[action] is 'build':
                    action_success = self.player.build_gate_action(action_params[0], action_params[1])

                if key_list[action] is 'summon':
                    # TODO:  allow multiple summons for black goat with Fertility Cult
                    action_success = self.player.summon_action(action_params[0], action_params[1])

                if key_list[action] is 'recruit':
                    action_success = self.player.recruit_cultist(action_params[1])

                if key_list[action] is 'combat':
                    action_success = self.player.combat_action(action_params[0], action_params[1], action_params[2])

            else:
                print("No Possible Actions!")
                self.player.spend_power(self.player.power)
                action_success = True
        self.player.free_action()
        self.player.take_spell_book()
        return action_success

    def weighted_choice_action(self):
        possible_builds = self.player.find_build_actions()
        possible_moves = self.player.find_move_actions(self.map)
        possible_captures = self.player.find_capture_actions()
        possible_summons = self.player.find_summon_actions()
        possible_recruits = self.player.find_recruit_actions()
        possible_combat = self.player.find_combat_actions()

        action_func = {
            'capture': [],
            'build': [],
            'move': [],
            'summon': [],
            'recruit': [],
            'combat': [],
            'awaken': [],
            'special': []
        }

        action_probability = {}

        if len(possible_captures) > 0:
            action_probability['capture'] = []
            action_probability['capture'].append(self._probability_dict['capture'])
            action_func['capture'] = possible_captures

        if len(possible_summons) > 0:
            action_probability['summon'] = []
            action_probability['summon'].append(self._probability_dict['summon'])
            action_func['summon'] = possible_summons

        if len(possible_moves) > 0:
            action_probability['move'] = []
            action_probability['move'].append(self._probability_dict['move'])
            action_func['move'] = possible_moves

        if len(possible_builds) > 0:
            action_probability['build'] = []
            action_probability['build'].append(self._probability_dict['build'])
            action_func['build'] = possible_builds

        if len(possible_recruits) > 0:
            action_probability['recruit'] = []
            action_probability['recruit'].append(self._probability_dict['recruit'])
            action_func['recruit'] = possible_recruits

        if len(possible_combat) > 0:
            action_probability['combat'] = []
            action_probability['combat'].append(self._probability_dict['combat'])
            action_func['combat'] = possible_combat

        action_success = False
        while action_success is False:
            if len(action_probability) > 0:
                key_list = []
                p_dist = []

                for k, v in action_probability.items():
                    p_dist.append(v[0])
                    key_list.append(k)
                p_norm = [float(i) / sum(p_dist) for i in p_dist]
                action = choice(range(len(key_list)), 1, p=p_norm)[0]
                action_params = action_func[key_list[action]][0]

                action_func.pop(key_list[action])
                action_probability.pop(key_list[action])

                if key_list[action] is 'capture':
                    action_success = self.player.capture_unit(action_params[0], action_params[1], action_params[2])

                if key_list[action] is 'move':
                    # TODO:  allow multiple moves
                    move_scores = [clamp(float(i[3]), 0, 10) for i in possible_moves]
                    move_total = sum(move_scores)
                    if move_total > 0:
                        move_scores_norm = [float(s) / move_total for s in move_scores]
                        move_choice = choice(range(len(possible_moves)), 1, p=move_scores_norm)[0]
                        action_success = self.player.move_action(possible_moves[move_choice][0],
                                                                 possible_moves[move_choice][1],
                                                                 possible_moves[move_choice][2])

                if key_list[action] is 'build':
                    action_success = self.player.build_gate_action(action_params[0], action_params[1])

                if key_list[action] is 'summon':
                    # TODO:  allow multiple summons for black goat with Fertility Cult
                    action_success = self.player.summon_action(action_params[0], action_params[1])

                if key_list[action] is 'recruit':
                    action_success = self.player.recruit_cultist(action_params[1])

                if key_list[action] is 'combat':
                    action_success = self.player.combat_action(action_params[0], action_params[1], action_params[2])

            else:
                print("No Possible Actions!")
                self.player.spend_power(self.player.power)
                action_success = True
        self.player.free_action()
        return action_success

    '''
    kill_unit
    remove a unit from the map and place it in the owners pool
    '''

    def kill_unit(self, unit):
        assert isinstance(unit, Unit)
        unit.set_unit_state(UnitState.in_reserve)
        unit.set_unit_zone(unit.faction._pool)
        return True

    def kill_from_selection(self, units):
        if len(units) > 1:
            if self._method is Methods.random:
                units = self.kill_from_selection_random(units)
            elif self._method is Methods.weighted_choice:
                units = self.kill_from_selection_wc(units)
        elif len(units) == 1:
            self.kill_unit(units[0])
            print(self.player._color + TextColor.BOLD + '%s %s has been killed!' % (
                units[0].faction._name, units[0].unit_type.value) + TextColor.ENDC)
            return []
        elif len(units) <= 0:
            print(TextColor.BOLD + 'Kill list empty'+ TextColor.ENDC)
        return units

    def kill_from_selection_random(self, units):
        index = choice(range(len(units)), 1)[0]
        unit_to_kill = units[index]
        assert isinstance(unit_to_kill, Unit)
        if unit_to_kill.unit_state is UnitState.in_play:
            self.kill_unit(unit_to_kill)
            units.remove(unit_to_kill)
            print(self.player._color + TextColor.BOLD + '%s %s has been killed!' % (unit_to_kill.faction._name, unit_to_kill.unit_type.value) + TextColor.ENDC)
        return units

    def kill_from_selection_wc(self, units):
        # weight based on combat power
        unit_weights = []
        for unit in units:
            assert isinstance(unit, Unit)
            unit_weights.append(unit.combat_power + 1)
        sum_unit_weights = sum(unit_weights)

        unit_weights_norm = [float(w) / sum_unit_weights for w in unit_weights]

        index = choice(range(len(units)), 1, p = unit_weights_norm )[0]

        unit_to_kill = units[index]
        assert isinstance(unit_to_kill, Unit)
        if unit_to_kill.unit_state is UnitState.in_play:
            self.kill_unit(unit_to_kill)
            units.remove(unit_to_kill)
            print(self.player._color + TextColor.BOLD + '%s %s has been killed!' % (unit_to_kill.faction._name, unit_to_kill.unit_type.value) + TextColor.ENDC)
        return units

    def pain_unit(self, unit):
        assert isinstance(unit, Unit)
        unit.set_unit_zone(unit.faction._home_zone)
        return True

    def pain_from_selection(self, units):
        # if self._method is Methods.random:
        # units = self.pain_from_selection_random(units)
        # elif self._method is Methods.weighted_choice:
        # units = self.pain_from_selection_wc(units)
        if len(units) > 1:
            if self._method is Methods.random:
                units = self.pain_from_selection_random(units)
            elif self._method is Methods.weighted_choice:
                units = self.pain_from_selection_wc(units)
        elif len(units) == 1:
            self.pain_unit(units[0])

            print(self.player._color + TextColor.BOLD + '%s %s has been pained!' % (
                units[0].faction._name, units[0].unit_type.value) + TextColor.ENDC)
            return []
        elif len(units) <= 0:
            print(TextColor.BOLD + 'Pain list empty'+ TextColor.ENDC)
            return []
        return []

    '''
    Pain methods
    Currently moves units to the home zone, but should employ move logic
    TODO: select a location to move pained units to
    '''
    def pain_from_selection_random(self, units):
        index = choice(range(len(units)), 1)[0]
        unit_to_kill = units[index]
        assert isinstance(unit_to_kill, Unit)
        if unit_to_kill.unit_state is UnitState.in_play:
            self.pain_unit(unit_to_kill)
            units.remove(unit_to_kill)
            print(self.player._color + TextColor.BOLD + '%s %s has been pained!' % (unit_to_kill.faction._name, unit_to_kill.unit_type.value) + TextColor.ENDC)
            return units
        return units

    def pain_from_selection_wc(self, units):
        # weight based on combat power
        unit_weights = []
        for unit in units:
            assert isinstance(unit, Unit)
            unit_weights.append(unit.combat_power + 1)
        sum_unit_weights = sum(unit_weights)

        unit_weights_norm = [float(w) / sum_unit_weights for w in unit_weights]

        index = choice(range(len(units)), 1, p=unit_weights_norm)[0]

        unit_to_kill = units[index]
        assert isinstance(unit_to_kill, Unit)
        if unit_to_kill.unit_state is UnitState.in_play:
            self.pain_unit(unit_to_kill)
            units.remove(unit_to_kill)
            print(self.player._color + TextColor.BOLD + '%s %s has been pained!' % (
            unit_to_kill.faction._name, unit_to_kill.unit_type.value) + TextColor.ENDC)
            return units
        return units

    def select_spell(self, spells):
        if self._method is Methods.random:
            self.select_spell_random(spells)
        elif self._method is Methods.weighted_choice:
            self.select_spell_wc(spells)

    def select_spell_random(self, spells):
        valid_spells = [i for i in range(len(self._spells)) if self._spells[i]['state'] == False]
        index = valid_spells[choice(range(len(valid_spells)), 1)[0]]
        self._spells[index]['state'] = True
        self._spells[index]['method']()
        print (self.player._color + TextColor.BOLD + "Spell selected: %s"%(self._spells[index]['name']) + TextColor.ENDC)
        return

    def select_spell_wc(self, spells):
        valid_spells = [i for i in range(len(self._spells)) if self._spells[i]['state'] == False]
        index = valid_spells[choice(range(len(valid_spells)), 1)[0]]
        self._spells[index]['state'] = True
        self._spells[index]['method']()
        print (self.player._color + TextColor.BOLD + "Spell selected: %s"%(self._spells[index]['name']) + TextColor.ENDC)
        return
