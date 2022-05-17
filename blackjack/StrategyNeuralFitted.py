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
from tensorflow.keras.losses import mean_squared_error

num_inputs = len(BlackjackState(0, False, Card(Face.Ace, Suit.Clubs)).__dict__)
num_outputs = len(Action)


class NeuralFittedStrategy(BlackjackStrategy):
    # Some of the following code was adapted from:
    #   Hands-on Machine Learning with Scikit-Learn, Keras & TensorFlow
    #     O'Reilly, ch18 - https://homl.info/
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
            inputs = game_state.to_array()
            q_values = self._model.predict(inputs)
            sorted_recommended_actions = np.argsort(q_values[0])
            best_legal_action = [x for x in sorted_recommended_actions if x in legal_actions][-1]
            return Action(best_legal_action)

    def update_policy(self, experience: BlackjackExperience):
        reward = self.determine_reward(experience.last_state.hand_state, experience.bet)
        NeuralFittedStrategy._experience_buffer.append((experience, reward))

    def _experience_replay(self, discount_factor=0.95, optimizer=Adam, loss_fn=mean_squared_error):
        if len(NeuralFittedStrategy._experience_buffer) < self._batch_size:
            print(f"Not enough experiences to sample a batch size of: {self._batch_size}")
            return
        random_samples = sample(NeuralFittedStrategy._experience_buffer, self._batch_size)
        experiences = np.array([random_sample[0] for random_sample in random_samples])
        rewards = np.array([random_sample[1] for random_sample in random_samples])

        # It would be nice to not loop through the experiences four times, later.
        actions = np.array([experience.action for experience in experiences])
        output_states = np.array([experience.resulting_state.to_array() for experience in experiences])
        input_states = np.array([experience.last_state.to_array() for experience in experiences])
        is_dones = np.array([
            TerminationStates.has_value(int(experience.resulting_state.hand_state)) for experience in experiences
        ])

        resulting_q_values = NeuralFittedStrategy._model.predict(output_states)
        # TODO: mask off the legal moves
        resulting_max_q_values = np.max(resulting_q_values, axis=1)
        target_q_values = (rewards + (1 - is_dones) * discount_factor * resulting_max_q_values)
        target_q_values = target_q_values.reshape(-1, 1)
        mask = tf.one_hot(actions, num_outputs)
        with tf.GradientTape() as tape:
            all_q_values = NeuralFittedStrategy._model(input_states[0:3])
            q_values = tf.reduce_sum(all_q_values * mask, axis=1, keepdims=True)
            loss = tf.reduce_mean(loss_fn(target_q_values, q_values))
        grads = tape.gradient(loss, NeuralFittedStrategy._model.trainable_variables)
        optimizer.apply_gradients(zip(grads, NeuralFittedStrategy._model.trainable_variables))

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
