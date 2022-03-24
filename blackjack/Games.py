from abc import ABC, abstractmethod
from blackjack.Cards import Deck, Card, Face
from enum import Enum
from blackjack.Policy import Action
from blackjack.Strategies import BlackjackStrategy, HitUntilNextCardBust, FixedStrategy, QLearningStrategy, qlp


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
        if game_class == 'FixedPolicyGame':
            return FixedPolicyGame()
        elif game_class == 'QLearningPolicyGame':
            return QLearningPolicyGame()
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

        # initialize states
        self._previous_state = None
        self._current_state = self.score_hand(self._player_hand)

        # default strategies
        self._dealer_strategy = HitUntilNextCardBust()
        self._player_strategy = FixedStrategy()

    def play(self) -> (Winner, int, int):
        while self.take_hit(self._dealer_hand, self._dealer_strategy):
            self._dealer_hand.append(self._deck.draw())

        while self.take_hit(self._player_hand, self._player_strategy):
            self._previous_state = self._current_state
            self._player_hand.append(self._deck.draw())
            self._current_state = self.score_hand(self._player_hand)
            self.update_policy()

        dealer_score = self.score_hand(self._dealer_hand)
        player_score = self.score_hand(self._player_hand)

        self._previous_state = self._current_state

        if player_score > 21:
            winner = Winner.Dealer  # player bust
            self._current_state = 'LOST/BUST'
        elif dealer_score > 21:
            winner = Winner.Player  # dealer bust
            self._current_state = 'WON'
        else:  # push goes to dealer here
            if player_score > dealer_score:
                winner = Winner.Player
                self._current_state = 'WON'
            else:
                winner = Winner.Dealer
                self._current_state = 'LOST/BUST'
        self.update_policy()

        return winner, dealer_score, player_score

    def update_policy(self):
        pass

    def take_hit(self, hand: BlackjackHand, strategy: BlackjackStrategy):
        current_score = self.score_hand(hand)
        if current_score > 21:
            return False
        action = strategy.evaluate(current_score, self._deck)
        return action == Action.HIT

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


class FixedPolicyGame(Game):
    def __init__(self):
        Game.__init__(self)
        self.set_strategies(dealer_strategy=HitUntilNextCardBust(), player_strategy=FixedStrategy())


class QLearningPolicyGame(Game):
    def __init__(self):
        Game.__init__(self)
        self.set_strategies(dealer_strategy=HitUntilNextCardBust(), player_strategy=QLearningStrategy())

    def update_policy(self):
        print(f"\tUpdate policy called: previous state: {self._previous_state} - current state: {self._current_state}.")
