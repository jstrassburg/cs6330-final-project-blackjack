from blackjack.Strategies import BlackjackStrategy, BlackjackState
from blackjack.Cards import Card
from blackjack.Policy import Action
from random import random, choice

# the .python might need to be removed at runtime
# it fixes code completion, however, due to:
#   https://github.com/tensorflow/tensorflow/issues/53144
from tensorflow.python import keras
from tensorflow.python.keras.layers import Dense

# Some of the following code was adapted from:
#   Hands-on Machine Learning with Scikit-Learn, Keras & TensorFlow
#     O'Reilly, ch18
num_inputs = len(BlackjackStrategy.__dict__)
num_outputs = len(Action)

model = keras.models.Sequential([
    Dense(32, activation='elu', input_shape=[num_inputs]),
    Dense(32, activation='elu'),
    Dense(num_outputs)
])


class NeuralFittedStrategy(BlackjackStrategy):
    def __init__(self, epsilon_value=0.1):
        self._epsilon = epsilon_value
        self._model = model

    def evaluate(self, game_state: BlackjackState) -> Action:
        if random() < self._epsilon:
            return choice(self._possible_actions(game_state))
        else:
            return self._best_action(game_state)

    def update_policy(self, previous_state, action, resulting_state, bet: int):
        pass

    def _possible_actions(self, game_state: BlackjackState):
        return list(Action)

    def _best_action(self, game_state: BlackjackState):
        return Action.STAND
