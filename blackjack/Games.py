from abc import ABC, abstractmethod
from blackjack.Cards import Deck, Card, Face
from enum import Enum
from itertools import product
from random import choice
from blackjack.Strategies import BlackjackStrategy, HitToSeventeenStrategy


BlackjackHand = list[Card]


class GameNotImplementedException(ValueError):
    pass


class Winner(Enum):
    Dealer = 1
    Player = 2
    DegenerateGambler = 2


class GamesFactory:
    @staticmethod
    def create(game_class):
        if game_class == 'SimplifiedGame':
            return SimplifiedGame()
        else:
            raise GameNotImplementedException()


class Game(ABC):
    def __init__(self):
        self._player_hand = BlackjackHand()
        self._dealer_hand = BlackjackHand()
        self._deck = Deck()

        # initialize hands
        self._player_hand.append(self._deck.draw())
        self._dealer_hand.append(self._deck.draw())
        self._player_hand.append(self._deck.draw())
        self._dealer_hand.append(self._deck.draw())

        # default strategies
        self._dealer_strategy = HitToSeventeenStrategy
        self._player_strategy = HitToSeventeenStrategy

    @abstractmethod
    def play(self):
        pass

    @staticmethod
    def score_hand(hand: BlackjackHand):
        score = 0
        aces = [x for x in hand if x == Face.Ace]
        non_aces = [x for x in hand if x != Face.Ace]
        score += sum([x.face_values()[0] for x in non_aces])
        ace_values = [x.face_values() for x in aces]
        ace_scores = sorted(set(sum([x for x in product(*ace_values)])))  # for 3 aces, this should be [3,13,23,33]
        ace_scores = [x for x in ace_scores if x <= 21]
        for ace_score in ace_scores:
            if (score + ace_score >= 17) and (score + ace_score < 22):
                # soft_hand = True, future potential enhancement
                return score + ace_score
        return score + min(ace_scores)

    def set_strategies(self, dealer_strategy: BlackjackStrategy, player_strategy: BlackjackStrategy):
        self._dealer_strategy = dealer_strategy
        self._player_strategy = player_strategy


class SimplifiedGame(Game):
    def __init__(self):
        Game.__init__(self)
        self.set_strategies(dealer_strategy=HitToSeventeenStrategy(), player_strategy=HitToSeventeenStrategy())

    def play(self):
        return choice([Winner.Player, Winner.Dealer])
