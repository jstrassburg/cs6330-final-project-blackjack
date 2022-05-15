from abc import ABC, abstractmethod
from blackjack.Policy import Action, FixedPolicy, QLearningPolicy, OptimizedPolicy
from blackjack.Cards import Card
from blackjack.States import TerminationStates
from random import random, choice
import numpy as np


class BlackjackState:
    def __init__(self, hand_state: int, is_soft_hand: bool, dealer_show_card: Card):
        self.hand_state = hand_state  # This is either the hand score or a TerminationState - refactor later?
        self.is_soft_hand = is_soft_hand
        self.dealer_show_card = dealer_show_card

    def to_array(self) -> np.array:
        return np.array([float(self.hand_state), float(self.is_soft_hand), float(self.dealer_show_card)])[np.newaxis, :]


class BlackjackExperience:
    def __init__(self, last_state: BlackjackState, action: Action, resulting_state: BlackjackState, bet: int):
        self.last_state = last_state
        self.action = action
        self.resulting_state = resulting_state
        self.bet = bet


class BlackjackStrategy(ABC):
    @abstractmethod
    def evaluate(self, game_state: BlackjackState) -> Action:
        pass

    @abstractmethod
    def update_policy(self, experience: BlackjackExperience):
        pass


class HitUntilSeventeen(BlackjackStrategy):
    def __init__(self, hit_soft_seventeen=True):
        self._hit_soft_seventeen = hit_soft_seventeen

    def evaluate(self, game_state: BlackjackState) -> Action:
        if game_state.hand_state == 17 and game_state.is_soft_hand and self._hit_soft_seventeen:
            return Action.HIT

        return Action.HIT if game_state.hand_state < 17 else Action.STAND

    def update_policy(self, experience: BlackjackExperience):
        pass


class FixedStrategy(BlackjackStrategy):
    def evaluate(self, game_state: BlackjackState) -> Action:
        return FixedPolicy[game_state.hand_state]

    def update_policy(self, experience: BlackjackExperience):
        pass


qlp = QLearningPolicy()


class QLearningStrategy(BlackjackStrategy):
    def __init__(self, epsilon_value=0.1, lambda_value=0.1, alpha_value=0.1):
        self._epsilon = epsilon_value
        self._lambda = lambda_value
        self._alpha = alpha_value
        self._policy = qlp

    def evaluate(self, game_state: BlackjackState) -> Action:
        if random() < self._epsilon:
            return choice(self._policy.possible_actions(game_state.hand_state))
        else:
            return self._policy.best_action(game_state.hand_state)

    def update_policy(self,  experience: BlackjackExperience):
        last_hand_state = experience.last_state.hand_state
        resulting_state = experience.resulting_state.hand_state
        action = experience.action
        bet = experience.bet

        reward = self.determine_reward(resulting_state, bet)
        current_q = self._policy.get_q_value(last_hand_state, action)
        high_resulting_q = self._policy.get_highest_q_value(resulting_state)
        new_q = (1 - self._alpha) * current_q + self._alpha * (reward + self._lambda * high_resulting_q)
        self._policy.update_q_value(last_hand_state, action, new_q)

    @staticmethod
    def determine_reward(hand_state, bet: int):
        if hand_state == TerminationStates.WON:
            return bet
        if hand_state in [TerminationStates.LOST, TerminationStates.BUST]:
            return -bet
        if hand_state == TerminationStates.PUSH:
            return bet / 2
        return hand_state


class OptimizedStrategy(BlackjackStrategy):
    def evaluate(self, game_state: BlackjackState) -> Action:
        return OptimizedPolicy[game_state.hand_state]

    def update_policy(self, experience: BlackjackExperience):
        pass
