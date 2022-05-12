from blackjack.Strategies import BlackjackStrategy, BlackjackState
from blackjack.Cards import Card
from blackjack.Policy import Action
from random import random, choice
import numpy as np
from collections import deque

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
    def __init__(self, epsilon_value=0.1, batch_size=50):
        self._epsilon = epsilon_value
        self._batch_size = batch_size
        self._model = model
        self._experience_buffer = deque(maxlen=1000)

    def evaluate(self, game_state: BlackjackState) -> Action:
        if random() < self._epsilon:
            return choice(self._possible_actions(game_state))
        else:
            q_values = self._model.predict(game_state)
            return Action(np.argmax(q_values[0]))

    def update_policy(self, previous_state, action, resulting_state, bet: int):
        pass

    def _possible_actions(self, game_state: BlackjackState):
        return list(Action)
