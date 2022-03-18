from abc import ABC, abstractmethod
from Cards import Deck
from enum import Enum
from random import choice


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


class Game:
    def __init__(self):
        self._player_hand = []
        self._dealer_hand = []
        self._deck = Deck()

        self._player_hand.append(self._deck.draw())
        self._dealer_hand.append(self._deck.draw())
        self._player_hand.append(self._deck.draw())
        self._dealer_hand.append(self._deck.draw())

    @abstractmethod
    def play(self):
        pass


class SimplifiedGame(Game):
    def __init__(self):
        Game.__init__(self)

    def play(self):
        return choice([Winner.Player, Winner.Dealer])
