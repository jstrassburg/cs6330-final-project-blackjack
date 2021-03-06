from blackjack.Cards import Deck, Face
from enum import Enum
from blackjack.Strategies import *
from blackjack.StrategyTreeBased import TreeBasedStrategy
from blackjack.States import TerminationStates

BlackjackHand = list[Card]


class GameNotImplementedException(ValueError):
    pass


class Winner(Enum):
    Push = 0
    Dealer = 1
    Player = 2
    DegenerateGambler = 2


class GamesFactory:
    @staticmethod
    def create(game_class, bet: int):
        if game_class == 'FixedPolicyGame':
            return FixedPolicyGame(bet)
        elif game_class == 'QLearningPolicyGame':
            return QLearningPolicyGame(bet)
        elif game_class == 'OptimizedPolicyGame':
            return OptimizedPolicyGame(bet)
        elif game_class == 'NeuralFittedPolicyGame':
            return NeuralFittedPolicyGame(bet)
        elif game_class == 'TreeBasedPolicyGame':
            return TreeBasedPolicyGame(bet)
        else:
            raise GameNotImplementedException()


class Game(ABC):
    def __init__(self, bet: int):
        self._bet = bet
        self._player_hand = BlackjackHand()
        self._dealer_hand = BlackjackHand()
        self._deck = Deck()

        # initialize hands
        self._player_hand.append(self._deck.draw())
        self._dealer_hand.append(self._deck.draw())
        self._player_hand.append(self._deck.draw())
        self._dealer_show_card = self._deck.draw()
        self._dealer_hand.append(self._dealer_show_card)

        # default strategies
        self._dealer_strategy = HitUntilSeventeen()
        self._player_strategy = FixedStrategy()

    def play(self) -> (Winner, int, int):
        # Take a rules structure, if we get that far with this stuff in it:
        hit_after_double = False
        double_after_hit = False
        action = None

        initial_player_hand_score = self.score_hand(self._player_hand)
        print(f"\tDealer shows: {self._dealer_show_card.face}")
        print(f"\tPlayer has {self._player_hand[0].face.name} and {self._player_hand[1].face.name} "
              f"for: {'soft ' if initial_player_hand_score[1] else ''}{initial_player_hand_score[0]}")

        last_player_hand = self._player_hand.copy()
        while action != Action.STAND:
            last_player_hand = self._player_hand.copy()
            last_action = action
            action = self.get_action(self._player_hand, self._player_strategy)

            # revert to HIT if we've already HIT
            if last_action == Action.HIT and action == Action.DOUBLE_DOWN and not double_after_hit:
                action = Action.HIT

            # double the bet for a DOUBLE_DOWN
            if action == Action.DOUBLE_DOWN:
                self._bet *= 2

            if action in [Action.HIT, Action.DOUBLE_DOWN]:
                drawn_card = self._deck.draw()
                print(f"\t{action} and got {drawn_card.face.name} of {drawn_card.suit.name}")
                self._player_hand.append(drawn_card)
                resulting_hand_state = self.determine_current_hand_state(action)
                if resulting_hand_state == TerminationStates.BUST:
                    print('Player BUST')
                    self.update_policy(last_player_hand, action, self._bet)
                    return Winner.Dealer, 0, self.score_hand(self._player_hand)[0]
                if action == Action.DOUBLE_DOWN and not hit_after_double:
                    break
                self.update_policy(last_player_hand, action, self._bet)

        while self.get_action(self._dealer_hand, self._dealer_strategy) == Action.HIT:
            self._dealer_hand.append(self._deck.draw())

        resulting_hand_state = self.determine_current_hand_state(action)

        dealer_score = self.score_hand(self._dealer_hand)[0]
        player_score = self.score_hand(self._player_hand)[0]
        self.update_policy(last_player_hand, action, self._bet)

        if resulting_hand_state == TerminationStates.PUSH:
            winner = Winner.Push
        else:
            winner = Winner.Player if resulting_hand_state == TerminationStates.WON else Winner.Dealer

        return winner, dealer_score, player_score

    def determine_current_hand_state(self, last_action):
        dealer_score = self.score_hand(self._dealer_hand)[0]
        player_score = self.score_hand(self._player_hand)[0]
        if player_score > 21:
            return TerminationStates.BUST
        if last_action in [Action.STAND, Action.DOUBLE_DOWN]:
            if dealer_score > 21:
                return TerminationStates.WON
            if dealer_score == player_score:
                return TerminationStates.PUSH
            return TerminationStates.WON if player_score > dealer_score else TerminationStates.LOST
        return player_score

    def update_policy(self, last_hand: BlackjackHand, action: Action, bet: int):
        last_hand_state, last_is_soft = self.score_hand(last_hand)
        resulting_hand_state = self.determine_current_hand_state(action)
        resulting_hand_score, resulting_is_soft = self.score_hand(self._player_hand)

        last_state = BlackjackState(last_hand_state, last_is_soft, self._dealer_show_card)
        resulting_state = BlackjackState(resulting_hand_state, resulting_is_soft, self._dealer_show_card)

        experience = BlackjackExperience(last_state, action, resulting_state, bet)

        print(f"\tUpdate policy called: last hand state: {last_hand_state} - "
              f"action: {action} - resulting state: {resulting_hand_state}.")
        self._player_strategy.update_policy(experience)

    def get_action(self, hand: BlackjackHand, strategy: BlackjackStrategy):
        current_score, is_soft_hand = self.score_hand(hand)
        if current_score > 21:
            return Action.STAND
        action = strategy.evaluate(BlackjackState(current_score, is_soft_hand, self._dealer_show_card))
        return action

    @staticmethod
    def score_hand(hand: BlackjackHand):
        score = 0
        if hand is None:
            return score
        score += sum([x.face_values()[0] for x in hand if x.face != Face.Ace])
        aces = [x for x in hand if x.face == Face.Ace]
        num_aces = len(aces)
        score += 11 * num_aces
        if score > 21:
            for i in range(num_aces):
                score -= 10
                aces.pop()
                if score <= 21:
                    return score, any(aces)
        return score, any(aces)

    def set_strategies(self, dealer_strategy: BlackjackStrategy, player_strategy: BlackjackStrategy):
        self._dealer_strategy = dealer_strategy
        self._player_strategy = player_strategy


class FixedPolicyGame(Game):
    def __init__(self, bet: int):
        Game.__init__(self, bet)
        self.set_strategies(dealer_strategy=HitUntilSeventeen(), player_strategy=FixedStrategy())


class QLearningPolicyGame(Game):
    def __init__(self, bet: int):
        Game.__init__(self, bet)
        self.set_strategies(dealer_strategy=HitUntilSeventeen(), player_strategy=QLearningStrategy())


class OptimizedPolicyGame(Game):
    def __init__(self, bet: int):
        Game.__init__(self, bet)
        self.set_strategies(dealer_strategy=HitUntilSeventeen(), player_strategy=OptimizedStrategy())


class NeuralFittedPolicyGame(Game):
    def __init__(self, bet: int):
        Game.__init__(self, bet)
        from blackjack.StrategyNeuralFitted import NeuralFittedStrategy
        self.set_strategies(dealer_strategy=HitUntilSeventeen(), player_strategy=NeuralFittedStrategy())


class TreeBasedPolicyGame(Game):
    def __init__(self, bet: int):
        Game.__init__(self, bet)
        self.set_strategies(dealer_strategy=HitUntilSeventeen(), player_strategy=TreeBasedStrategy())
