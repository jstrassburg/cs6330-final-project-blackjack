from abc import ABC, abstractmethod
from blackjack.Policy import Action, FixedPolicy, QLearningPolicy, OptimizedPolicy
from blackjack.Cards import Card
from blackjack.States import TerminationStates
from random import random, choice


class BlackjackStrategy(ABC):
    @abstractmethod
    def evaluate(self, hand_score: int, is_soft_hand: bool, dealer_show_card: Card) -> Action:
        pass

    @abstractmethod
    def update_policy(self, previous_state, action, resulting_state, bet: int):
        pass


class HitUntilSeventeen(BlackjackStrategy):
    def __init__(self, hit_soft_seventeen=True):
        self._hit_soft_seventeen = hit_soft_seventeen

    def evaluate(self, hand_score: int, is_soft_hand: bool, dealer_show_card: Card = None) -> Action:
        if hand_score == 17 and is_soft_hand and self._hit_soft_seventeen:
            return Action.HIT

        return Action.HIT if hand_score < 17 else Action.STAND

    def update_policy(self, previous_state, action, resulting_state, bet: int):
        pass


class FixedStrategy(BlackjackStrategy):
    def evaluate(self, hand_score: int, is_soft_hand: bool, dealer_show_card: Card) -> Action:
        return FixedPolicy[hand_score]

    def update_policy(self, previous_state, action, resulting_state, bet: int):
        pass


qlp = QLearningPolicy()


class QLearningStrategy(BlackjackStrategy):
    def __init__(self, epsilon_value=0.1, lambda_value=0.1, alpha_value=0.1):
        self._epsilon = epsilon_value
        self._lambda = lambda_value
        self._alpha = alpha_value
        self._policy = qlp

    def evaluate(self, hand_score: int, is_soft_hand: bool, dealer_show_card: Card) -> Action:
        if random() < self._epsilon:
            return choice(self._policy.possible_actions(hand_score))
        else:
            return self._policy.best_action(hand_score)

    def update_policy(self, previous_state, action, resulting_state, bet: int):
        reward = self.determine_reward(resulting_state, bet)
        current_q = self._policy.get_q_value(previous_state, action)
        high_resulting_q = self._policy.get_highest_q_value(resulting_state)
        new_q = (1 - self._alpha) * current_q + self._alpha * (reward + self._lambda * high_resulting_q)
        self._policy.update_q_value(previous_state, action, new_q)

    @staticmethod
    def determine_reward(state, bet: int):
        if state == TerminationStates.WON:
            return bet
        if state in [TerminationStates.LOST, TerminationStates.BUST]:
            return -bet
        if state == TerminationStates.PUSH:
            return bet / 2
        return state


class OptimizedStrategy(BlackjackStrategy):
    def evaluate(self, hand_score: int, is_soft_hand: bool, dealer_show_card: Card) -> Action:
        return OptimizedPolicy[hand_score]

    def update_policy(self, previous_state, action, resulting_state, bet: int):
        pass
