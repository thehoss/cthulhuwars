from enum import Enum

from cthulhuwars.Maps import Map
from numpy.random import choice

class Methods(Enum):
    random = 0
    weighted_choice = 1

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

class PlayerLogic(object):
    def __init__(self, player, the_map):
        assert isinstance(the_map, Map)

        self.player = player
        self._method = Methods.random
        self.map    = the_map
        self.probability_dict = {
            'capture': 0.3,
            'build': 0.25,
            'move': 0.25,
            'summon': 0.1,
            'recruit': 0.1,
            'combat': 0,
            'awaken': 0,
            'special': 0
        }

    def use_method_random(self):
        self._method = Methods.random

    def use_method_wc(self):
        self._method = Methods.weighted_choice


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
            'summon': [],
            'move': [],
            'build': [],
            'recruit': [],
            'combat': [],
            'awaken': [],
            'special': []
        }

        action_probability = {}

        if len(possible_captures) > 0:
            action_probability['capture'] = []
            action_probability['capture'].append(self.probability_dict['capture'])
            action_func['capture'] = possible_captures

        if len(possible_summons) > 0:
            action_probability['summon'] = []
            action_probability['summon'].append(self.probability_dict['summon'])
            action_func['summon'] = possible_summons

        if len(possible_moves) > 0:
            action_probability['move'] = []
            action_probability['move'].append(self.probability_dict['move'])
            action_func['move'] = possible_moves

        if len(possible_builds) > 0:
            action_probability['build'] = []
            action_probability['build'].append(self.probability_dict['build'])
            action_func['build'] = possible_builds

        if len(possible_recruits) > 0:
            action_probability['recruit'] = []
            action_probability['recruit'].append(self.probability_dict['recruit'])
            action_func['recruit'] = possible_recruits

        if len(possible_combat) > 0:
            action_probability['combat'] = []
            action_probability['combat'].append(self.probability_dict['combat'])
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
                    move_choice = choice(range(len(possible_moves)), 1)[0]
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
                    action_success = self.player.combat_action(action_params[0], action_params[1], action_params[2] )

            else:
                print("No Possible Actions!")
                self.player.spend_power(self.player.power)
                action_success = True
        self.player.free_action()
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
            'summon': [],
            'move': [],
            'build': [],
            'recruit': [],
            'combat': [],
            'awaken': [],
            'special': []
        }

        action_probability = {}

        if len(possible_captures) > 0:
            action_probability['capture'] = []
            action_probability['capture'].append(self.probability_dict['capture'])
            action_func['capture'] = possible_captures

        if len(possible_summons) > 0:
            action_probability['summon'] = []
            action_probability['summon'].append(self.probability_dict['summon'])
            action_func['summon'] = possible_summons

        if len(possible_moves) > 0:
            action_probability['move'] = []
            action_probability['move'].append(self.probability_dict['move'])
            action_func['move'] = possible_moves

        if len(possible_builds) > 0:
            action_probability['build'] = []
            action_probability['build'].append(self.probability_dict['build'])
            action_func['build'] = possible_builds

        if len(possible_recruits) > 0:
            action_probability['recruit'] = []
            action_probability['recruit'].append(self.probability_dict['recruit'])
            action_func['recruit'] = possible_recruits

        if len(possible_combat) > 0:
            action_probability['combat'] = []
            action_probability['combat'].append(self.probability_dict['combat'])
            action_func['combat'] = possible_combat

        action_success = False
        while action_success is False:
            if len(action_probability) > 0:
                key_list = []
                p_dist = []

                for k, v in action_probability.iteritems():
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
                        action_success = self.player.move_action(possible_moves[move_choice][0], possible_moves[move_choice][1],
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