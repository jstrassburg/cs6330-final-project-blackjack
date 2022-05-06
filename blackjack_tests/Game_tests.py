import unittest

from blackjack.Cards import Card, Face, Suit
from blackjack.Games import Game


class TestGame(unittest.TestCase):
    def test_score_no_hand(self):
        actual = Game.score_hand([])
        expected = 0, False
        self.assertEqual(actual, expected)

    def test_score_one_non_ace(self):
        card = Card(Face.Ten, Suit.Hearts)
        actual = Game.score_hand([card])
        expected = 10, False
        self.assertEqual(actual, expected)

    def test_score_many_non_aces(self):
        card0 = Card(Face.Five, Suit.Hearts)
        card1 = Card(Face.Six, Suit.Spades)
        card2 = Card(Face.Jack, Suit.Clubs)
        hand = [card0, card1, card2]
        actual = Game.score_hand(hand)
        expected = 21, False
        self.assertEqual(actual, expected)

    def test_score_one_ace(self):
        card = Card(Face.Ace, Suit.Diamonds)
        actual = Game.score_hand([card])
        expected = 11, True
        self.assertEqual(actual, expected)

    def test_score_bust_ace_if_11(self):
        card0 = Card(Face.Ace, Suit.Hearts)
        card1 = Card(Face.Six, Suit.Spades)
        card2 = Card(Face.Jack, Suit.Clubs)
        hand = [card0, card1, card2]
        actual = Game.score_hand(hand)
        expected = 17, False
        self.assertEqual(actual, expected)

    def test_bust_hand(self):
        card0 = Card(Face.Queen, Suit.Spades)
        card1 = Card(Face.Six, Suit.Spades)
        card2 = Card(Face.Jack, Suit.Clubs)
        hand = [card0, card1, card2]
        actual = Game.score_hand(hand)
        expected = 26, False
        self.assertEqual(actual, expected)

    def test_bust_hand_with_aces(self):
        card0 = Card(Face.Five, Suit.Hearts)
        card1 = Card(Face.Seven, Suit.Spades)
        card2 = Card(Face.Ace, Suit.Clubs)
        card3 = Card(Face.Jack, Suit.Clubs)
        hand = [card0, card1, card2, card3]
        actual = Game.score_hand(hand)
        expected = 23, False
        self.assertEqual(actual, expected)

    def test_many_aces(self):
        card0 = Card(Face.Ace, Suit.Hearts)
        card1 = Card(Face.Ace, Suit.Spades)
        card2 = Card(Face.Ace, Suit.Clubs)
        card3 = Card(Face.Ace, Suit.Diamonds)
        hand = [card0, card1, card2, card3]
        actual = Game.score_hand(hand)
        expected = 14, True
        self.assertEqual(actual, expected)

    def test_soft_seventeen(self):
        card0 = Card(Face.Ace, Suit.Hearts)
        card1 = Card(Face.Six, Suit.Spades)
        hand = [card0, card1]
        actual = Game.score_hand(hand)
        expected = 17, True
        self.assertEqual(actual, expected)