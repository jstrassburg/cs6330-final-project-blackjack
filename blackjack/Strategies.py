from abc import ABC, abstractmethod
from enum import Enum
from blackjack.Cards import Card, Deck


class Action(Enum):
    HIT = 1
    STAND = 2


class BlackjackStrategy(ABC):
    @abstractmethod
    def evaluate(self, hand_score: int, deck: Deck) -> Action:
        pass


class HitUntilNextCardBust(BlackjackStrategy):
    def evaluate(self, hand_score: int, deck: Deck) -> Action:
        next_card = deck.peek()
        return Action.HIT if hand_score + next_card.face_values()[0] < 22 else Action.STAND


class HitToSeventeenStrategy(BlackjackStrategy):
    def evaluate(self, hand_score: int, deck: Deck = None) -> Action:
        return Action.HIT if hand_score < 17 else Action.STAND
