from blackjack.Strategies import BlackjackStrategy, BlackjackState
from blackjack.Cards import Card
from blackjack.Policy import Action


class TreeBasedStrategy(BlackjackStrategy):
    def evaluate(self, game_state: BlackjackState) -> Action:
        pass

    def update_policy(self, previous_state, action, resulting_state, bet: int):
        pass
