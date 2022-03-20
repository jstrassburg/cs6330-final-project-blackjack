from abc import ABC, abstractmethod
from enum import Enum
from Cards import Card


class Action(Enum):
    HIT = 1
    STAND = 2


class BlackjackStrategy(ABC):
    @abstractmethod
    def evaluate(self, hand_score: int, dealer_shows: Card) -> Action:
        pass


class HitToSeventeenStrategy(BlackjackStrategy):
    def evaluate(self, hand_score: int, dealer_shows: Card = None) -> Action:
        return Action.HIT if hand_score < 17 else Action.STAND


class HitUntilBeatingDealerShowPlusTen(BlackjackStrategy):
    def evaluate(self, hand_score: int, dealer_shows: Card) -> Action:
        score_to_beat = max(dealer_shows.face_values()) + 10
        return Action.HIT if hand_score < score_to_beat else Action.STAND
