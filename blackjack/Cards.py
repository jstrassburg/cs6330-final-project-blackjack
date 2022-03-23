from enum import Enum
from random import shuffle


class DeckEmptyException(Exception):
    pass


class Suit(Enum):
    Hearts = 'Hearts'
    Diamonds = 'Diamonds'
    Spades = 'Spades'
    Clubs = 'Clubs'


class Face(Enum):
    Ace = {'name': 'Ace', 'values': [1, 11]}
    Two = {'name': 'Two', 'values': [2]}
    Three = {'name': 'Three', 'values': [3]}
    Four = {'name': 'Four', 'values': [4]}
    Five = {'name': 'Five', 'values': [5]}
    Six = {'name': 'Six', 'values': [6]}
    Seven = {'name': 'Seven', 'values': [7]}
    Eight = {'name': 'Eight', 'values': [8]}
    Nine = {'name': 'Nine', 'values': [9]}
    Ten = {'name': 'Ten', 'values': [10]}
    Jack = {'name': 'Jack', 'values': [10]}
    Queen = {'name': 'Queen', 'values': [10]}
    King = {'name': 'King', 'values': [10]}


class Card:
    def __init__(self, face: Face, suit: Suit):
        self.face = face
        self.suit = suit

    def face_values(self):
        return self.face.value['values']

    def name(self):
        return self.face.value['name']


class Deck:
    def __init__(self):
        self._deck = list()
        self.reset_and_shuffle()

    def shuffle(self):
        shuffle(self._deck)

    def reset_and_shuffle(self):
        self._deck.clear()
        for face in Face:
            for suit in Suit:
                card = Card(face, suit)
                self._deck.append(card)
        self.shuffle()

    def count(self):
        return len(self._deck)

    def draw(self):
        if not self._deck:
            raise DeckEmptyException
        return self._deck.pop(0)

    def peek(self) -> Card:
        if not self._deck:
            raise DeckEmptyException
        return self._deck[0]
