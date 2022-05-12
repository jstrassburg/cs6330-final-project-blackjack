from blackjack.Strategies import BlackjackStrategy, BlackjackExperience
from blackjack.Cards import Card
from blackjack.Policy import Action


class TreeBasedStrategy(BlackjackStrategy):
    def evaluate(self, experience: BlackjackExperience) -> Action:
        pass

    def update_policy(self, previous_state, action, resulting_state, bet: int):
        pass
