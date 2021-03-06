from enum import Enum
from blackjack.States import TerminationStates


class Action(Enum):
    HIT = 0
    STAND = 1
    DOUBLE_DOWN = 2
    # SPLIT = 3

    def __int__(self):
        return self.value

    def __float__(self):
        return float(self.value)


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
    14: Action.HIT,
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
        for state in list(range(1, 10)):
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
        for state in list(range(10, 12)):
            self._q_table[state] = {
                'Actions': [
                    {
                        'Action': Action.STAND,
                        'Q': 0
                    },
                    {
                        'Action': Action.HIT,
                        'Q': 0
                    },
                    {
                        'Action': Action.DOUBLE_DOWN,
                        'Q': 0
                    }
                ]
            }
        for state in list(range(12, 22)):
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
        for state in [TerminationStates.BUST, TerminationStates.LOST, TerminationStates.WON, TerminationStates.PUSH]:
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

    def get_highest_q_value(self, state):
        return max([x['Q'] for x in self._q_table[state]['Actions']])

    def get_q_value(self, state, action: Action):
        return [x['Q'] for x in self._q_table[state]['Actions'] if x['Action'] == action][0]  # should only be one

    def update_q_value(self, state, action: Action, new_q):
        [x for x in self._q_table[state]['Actions'] if x['Action'] == action][0]['Q'] = new_q

    def best_action(self, state):
        actions = self._q_table[state]['Actions']
        best_q = float('-inf')
        best_action = actions[0]['Action']
        for action in actions:
            if action['Q'] > best_q:
                best_q = action['Q']
                best_action = action['Action']
        return best_action

    def get_table(self):
        return self._q_table


OptimizedPolicy = {
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
    14: Action.HIT,
    15: Action.HIT,
    16: Action.HIT,
    17: Action.STAND,
    18: Action.STAND,
    19: Action.STAND,
    20: Action.STAND,
    21: Action.STAND
}
