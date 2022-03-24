from enum import Enum


class Action(Enum):
    HIT = 1
    STAND = 2


FixedPolicy = {
    1: Action.HIT,
    2: Action.HIT,
    3: Action.HIT,
    4: Action.HIT,
    5: Action.HIT,
    6: Action.HIT,
    7: Action.HIT,
    8: Action.HIT,
    9: Action.HIT,
    10: Action.HIT,
    11: Action.HIT,
    12: Action.HIT,
    13: Action.HIT,
    14: Action.STAND,
    15: Action.STAND,
    16: Action.STAND,
    17: Action.STAND,
    18: Action.STAND,
    19: Action.STAND,
    20: Action.STAND,
    21: Action.STAND
}


class QLearningPolicy:
    def __init__(self):
        self._init_q_table()

    def _init_q_table(self):
        self._q_table = {}
        for state in list(range(1, 22)):
            self._q_table[state] = {
                'Actions': [
                    {
                        'Action': Action.STAND,
                        'Q': 0
                    },
                    {
                        'Action': Action.HIT,
                        'Q': 0
                    }
                ]
            }
        for state in ['WON', 'LOST/BUST']:
            self._q_table[state] = {
                'Actions': [
                    {
                        'Action': Action.STAND,
                        'Q': 0
                    }
                ]
            }

    def possible_actions(self, state):
        return [x['Action'] for x in self._q_table[state]['Actions']]

    def best_action(self, state):
        actions = self._q_table[state]['Actions']
        best_q = 0
        best_action = actions[0]['Action']
        for action in actions:
            if action['Q'] > best_q:
                best_q = action['Q']
                best_action = action['Action']
        return best_action
