from blackjack.Strategies import BlackjackStrategy, BlackjackState, BlackjackExperience
from blackjack.Cards import Card, Face, Suit
from blackjack.Policy import Action
from blackjack.States import TerminationStates
from blackjack.Filters import legal_move_filter
from random import random, choice, sample
import numpy as np
from collections import deque

import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD, RMSprop, Adam, Nadam
from tensorflow.keras.losses import mean_squared_error, mean_absolute_error

num_inputs = len(BlackjackState(0, False, Card(Face.Ace, Suit.Clubs)).__dict__)
num_outputs = len(Action)

EXPL_MAX = 1.0
EXPL_MIN = 0.05
EXPL_DECAY = 0.96


class NeuralFittedStrategy(BlackjackStrategy):
    # Some of the following code was adapted from:
    #   Hands-on Machine Learning with Scikit-Learn, Keras & TensorFlow
    #     O'Reilly, ch18 - https://homl.info/
    _experience_buffer = deque(maxlen=1000)
    _exploration_rate = EXPL_MAX
    _model = Sequential([
        Dense(32, activation='elu', input_shape=[num_inputs]),
        Dense(32, activation='elu'),
        Dense(num_outputs)
    ])
    _model.summary()
    _model.compile(Adam(learning_rate=1e-2), mean_absolute_error)

    def __init__(self, batch_size=50):
        self._batch_size = batch_size
        if len(NeuralFittedStrategy._experience_buffer) >= self._batch_size:
            self._experience_replay()

    def evaluate(self, game_state: BlackjackState) -> Action:
        if random() < NeuralFittedStrategy._exploration_rate:
            random_action = Action(choice(legal_move_filter(game_state)))
            print(f"\t\tRandom selected action: {random_action}")
            return random_action
        else:
            legal_actions = legal_move_filter(game_state)
            inputs = game_state.to_array()
            q_values = self._model.predict(self.scale_state(inputs[np.newaxis]))
            recommended_action = np.argmax(q_values[0])
            best_legal_action = Action(recommended_action)
            print(f"\t\tNetwork selected action: {best_legal_action}")
            if recommended_action in legal_actions:
                return best_legal_action
            if best_legal_action == Action.DOUBLE_DOWN:
                return Action.HIT
            return Action.STAND

    def update_policy(self, experience: BlackjackExperience):
        reward = self.determine_reward(experience.resulting_state.hand_state, experience.bet)
        NeuralFittedStrategy._experience_buffer.append((experience, reward))

    def _experience_replay(self, discount_factor=0.95):
        if len(NeuralFittedStrategy._experience_buffer) < self._batch_size:
            print(f"Not enough experiences to sample a batch size of: {self._batch_size}")
            return

        random_samples = sample(NeuralFittedStrategy._experience_buffer, self._batch_size)

        experiences = np.array([random_sample[0] for random_sample in random_samples])
        rewards = np.array([random_sample[1] for random_sample in random_samples])

        actions = np.array([int(experience.action) for experience in experiences])
        resulting_states = np.array([experience.resulting_state.to_array() for experience in experiences])
        last_states = np.array([experience.last_state.to_array() for experience in experiences])

        resulting_q_values = NeuralFittedStrategy._model.predict(self.scale_state(resulting_states))
        resulting_max_q_values = np.max(resulting_q_values, axis=1)
        target_q_values = (rewards + discount_factor * resulting_max_q_values)
        target_q_values = target_q_values.reshape(-1, 1)
        mask = tf.one_hot(actions, num_outputs)
        new_q_values = target_q_values * mask
        NeuralFittedStrategy._model.fit(self.scale_state(last_states), new_q_values, verbose=0)

        NeuralFittedStrategy._exploration_rate = max(
            NeuralFittedStrategy._exploration_rate * EXPL_DECAY, EXPL_MIN)

    @staticmethod
    def determine_reward(hand_state, bet: int):
        if hand_state == TerminationStates.WON:
            return bet
        if hand_state in [TerminationStates.LOST, TerminationStates.BUST]:
            return -bet
        if hand_state == TerminationStates.PUSH:
            return bet / 2
        return hand_state

    @staticmethod
    def scale_state(state):
        return state / np.array([25, 1, 11])
