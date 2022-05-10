from blackjack.Strategies import BlackjackStrategy
from blackjack.Cards import Card
from blackjack.Policy import Action


class NeuralFittedStrategy(BlackjackStrategy):
    def evaluate(self, hand_score: int, is_soft_hand: bool, dealer_show_card: Card) -> Action:
        pass

    def update_policy(self, previous_state, action, resulting_state, bet: int):
        pass
