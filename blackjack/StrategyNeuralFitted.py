from blackjack.Strategies import BlackjackStrategy, BlackjackState, BlackjackExperience
from blackjack.Policy import Action
from blackjack.States import TerminationStates
from blackjack.Filters import legal_move_filter
from random import random, choice, sample
import numpy as np
from collections import deque

# the .python might need to be removed at runtime
# it fixes code completion, however, due to:
#   https://github.com/tensorflow/tensorflow/issues/53144
from tensorflow.python import keras
from tensorflow.python.keras.layers import Dense

num_inputs = len(BlackjackStrategy.__dict__)
num_outputs = len(Action)


class NeuralFittedStrategy(BlackjackStrategy):
    # Some of the following code was adapted from:
    #   Hands-on Machine Learning with Scikit-Learn, Keras & TensorFlow
    #     O'Reilly, ch18
    _experience_buffer = deque(maxlen=1000)
    _model = keras.models.Sequential([
        Dense(32, activation='elu', input_shape=[num_inputs]),
        Dense(32, activation='elu'),
        Dense(num_outputs)
    ])

    def __init__(self, epsilon_value=0.1, batch_size=50):
        self._epsilon = epsilon_value
        self._batch_size = batch_size
        if len(NeuralFittedStrategy._experience_buffer) >= self._batch_size:
            self._experience_replay()

    def evaluate(self, game_state: BlackjackState) -> Action:
        if random() < self._epsilon:
            return choice(legal_move_filter(game_state))
        else:
            q_values = self._model.predict(game_state)
            return Action(np.argmax(q_values[0]))

    def update_policy(self, experience: BlackjackExperience):
        reward = self.determine_reward(experience.last_state, experience.bet)
        NeuralFittedStrategy._experience_buffer.append((experience, reward))

    def _experience_replay(self):
        if len(NeuralFittedStrategy._experience_buffer) < self._batch_size:
            print(f"Not enough experiences to sample a batch size of: {self._batch_size}")
            return
        random_sample = sample(NeuralFittedStrategy._experience_buffer, self._batch_size)
        # TODO: Train network

    @staticmethod
    def determine_reward(hand_state, bet: int):
        if hand_state == TerminationStates.WON:
            return bet
        if hand_state in [TerminationStates.LOST, TerminationStates.BUST]:
            return -bet
        if hand_state == TerminationStates.PUSH:
            return bet / 2
        return hand_state

