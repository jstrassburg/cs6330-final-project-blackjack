from blackjack.Strategies import BlackjackStrategy, BlackjackExperience
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
model = keras.models.Sequential([
    Dense(32, input_shape=[3])
])


class NeuralFittedStrategy(BlackjackStrategy):
    def __init__(self, epsilon_value=0.1):
        self._epsilon = epsilon_value
        self._model = model

    def evaluate(self, experience: BlackjackExperience) -> Action:
        if random() < self._epsilon:
            return choice(self._possible_actions(experience.hand_score))
        else:
            return self._best_action(experience)

    def update_policy(self, previous_state, action, resulting_state, bet: int):
        pass

    def _possible_actions(self, hand_score: int):
        return list(Action)

    def _best_action(self, experience: BlackjackExperience):
        return Action.STAND
