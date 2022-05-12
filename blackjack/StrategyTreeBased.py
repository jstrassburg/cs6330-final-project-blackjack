from random import Random
from blackjack.Strategies import BlackjackStrategy, BlackjackState
from blackjack.Cards import Card
from blackjack.Policy import Action
from sklearn.ensemble import RandomForestRegressor
from collections import deque

model = RandomForestRegressor()


class TreeBasedStrategy(BlackjackStrategy):
    def __init__(self, gamma=0.95,
                 learning_rate=0.001, mem_size=1000,
                 batch_size=20, exploration_max=1.0,
                 exploration_min=0.05, exploration_decay=0.96):
        self._model = model
        self._experience_buffer = deque(maxlen=mem_size)
        self._batch_size = batch_size

    def evaluate(self, game_state: BlackjackState) -> Action:
        pass

    def update_policy(self, previous_state, action, resulting_state, bet: int):
        pass

    def _remember(self):
        pass

    def _experience_replay(self):
        pass