from abc import ABC, abstractmethod
from blackjack.Policy import Action, FixedPolicy, QLearningPolicy
from blackjack.Cards import Deck
from random import random, choice


class BlackjackStrategy(ABC):
    @abstractmethod
    def evaluate(self, hand_score: int, deck: Deck) -> Action:
        pass


class HitUntilNextCardBust(BlackjackStrategy):
    def evaluate(self, hand_score: int, deck: Deck) -> Action:
        next_card = deck.peek()
        return Action.HIT if hand_score + min(next_card.face_values()) < 22 else Action.STAND


class FixedStrategy(BlackjackStrategy):
    def evaluate(self, hand_score: int, deck: Deck = None) -> Action:
        return FixedPolicy[hand_score]


qlp = QLearningPolicy()


class QLearningStrategy(BlackjackStrategy):
    def __init__(self, epsilon_value=0.9, lambda_value=0.1, alpha_value=0.1):
        self._epsilon = epsilon_value
        self._lambda = lambda_value
        self._alpha = alpha_value
        self._policy = qlp

    def evaluate(self, hand_score: int, deck: Deck) -> Action:
        if random() < self._epsilon:
            return choice(self._policy.possible_actions(hand_score))
        else:
            return self._policy.best_action(hand_score)
