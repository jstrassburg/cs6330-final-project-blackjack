from blackjack.Strategies import BlackjackStrategy, BlackjackState, BlackjackExperience
from blackjack.Cards import Card, Face, Suit
from blackjack.Policy import Action
from blackjack.States import TerminationStates
from blackjack.Filters import legal_move_filter
from random import random, choice, sample
import numpy as np
from collections import deque

# the .python might need to be removed at runtime
# it fixes code completion, however, due to:
#   https://github.com/tensorflow/tensorflow/issues/53144
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

num_inputs = len(BlackjackState(0, False, Card(Face.Ace, Suit.Clubs)).__dict__)
num_outputs = len(Action)


class NeuralFittedStrategy(BlackjackStrategy):
    # Some of the following code was adapted from:
    #   Hands-on Machine Learning with Scikit-Learn, Keras & TensorFlow
    #     O'Reilly, ch18
    _experience_buffer = deque(maxlen=1000)
    _model = Sequential([
        Dense(32, activation='elu', input_shape=[num_inputs]),
        Dense(32, activation='elu'),  # elu [exponential linear unit] to diminish the vanishing gradient problem
        Dense(num_outputs, activation='softmax')  # softmax to normalize outputs to probabilities that sum to 1
    ])
    _model.summary()

    def __init__(self, epsilon_value=0.1, batch_size=50):
        self._epsilon = epsilon_value
        self._batch_size = batch_size
        if len(NeuralFittedStrategy._experience_buffer) >= self._batch_size:
            self._experience_replay()

    def evaluate(self, game_state: BlackjackState) -> Action:
        if random() < self._epsilon:
            return choice(legal_move_filter(game_state))
        else:
            legal_actions = legal_move_filter(game_state)
            q_values = self._model.predict(game_state)
            sorted_recommended_actions = np.argsort(q_values[0])
            best_legal_action = [x for x in sorted_recommended_actions if x in legal_actions][-1]
            return best_legal_action

    def update_policy(self, experience: BlackjackExperience):
        reward = self.determine_reward(experience.last_state, experience.bet)
        NeuralFittedStrategy._experience_buffer.append((experience, reward))

    def _experience_replay(self, discount_factor=0.95, optimizer=Adam):
        if len(NeuralFittedStrategy._experience_buffer) < self._batch_size:
            print(f"Not enough experiences to sample a batch size of: {self._batch_size}")
            return
        random_sample = sample(NeuralFittedStrategy._experience_buffer, self._batch_size)
        experiences = np.array([random_sample[0] for _ in random_sample])
        rewards = np.array([random_sample[1] for _ in random_sample])
        last_states = np.array([experience.last_state for experience in experiences])
        resulting_states = np.array([experience.resulting_state for experience in experiences])
        input_states = [[x.hand_state, int(x.is_soft_hand), int(x.dealer_show_card)] for x in resulting_states]
        resulting_q_values = NeuralFittedStrategy._model.predict(input_states)
        # TODO: mask off the legal moves
        resulting_max_q_values = np.max(resulting_q_values, axis=1)
        
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
