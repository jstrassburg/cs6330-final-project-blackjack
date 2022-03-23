from abc import ABC, abstractmethod
from blackjack.Policy import Action, FixedPolicy
from blackjack.Cards import Deck


class BlackjackStrategy(ABC):
    @abstractmethod
    def evaluate(self, hand_score: int, deck: Deck) -> Action:
        pass


class HitUntilNextCardBust(BlackjackStrategy):
    def evaluate(self, hand_score: int, deck: Deck) -> Action:
        next_card = deck.peek()
        return Action.HIT if hand_score + max(next_card.face_values()) < 22 else Action.STAND


class FixedPolicyStrategy(BlackjackStrategy):
    def evaluate(self, hand_score: int, deck: Deck = None) -> Action:
        return FixedPolicy[hand_score]


class QLearningPolicyStrategy(BlackjackStrategy):
    def __init__(self, epsilon_value=0.1, lambda_value=0.1, alpha_value=0.1):
        self._epsilon = epsilon_value
        self._lambda = lambda_value
        self._alpha = alpha_value

    def evaluate(self, hand_score: int, deck: Deck) -> Action:
        pass
