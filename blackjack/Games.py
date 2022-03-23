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
        if hand is None:
            return score
        score += sum([x.face_values()[0] for x in hand if x.face != Face.Ace])
        aces = [x for x in hand if x.face == Face.Ace]
        score += 11 * len(aces)
        if score > 21:
            for _ in aces:
                score -= 10
                if score <= 21:
                    return score
        return score

    def set_strategies(self, dealer_strategy: BlackjackStrategy, player_strategy: BlackjackStrategy):
        self._dealer_strategy = dealer_strategy
        self._player_strategy = player_strategy


class SimplifiedGame(Game):
    def __init__(self):
        Game.__init__(self)
        self.set_strategies(dealer_strategy=HitToSeventeenStrategy(), player_strategy=HitToSeventeenStrategy())

    def play(self):
        return choice([Winner.Player, Winner.Dealer])
