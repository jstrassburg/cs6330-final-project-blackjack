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
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD, RMSprop, Adam, Nadam
from tensorflow.keras.losses import mean_squared_error, mean_absolute_error

num_inputs = len(BlackjackState(0, False, Card(Face.Ace, Suit.Clubs)).__dict__)
num_outputs = len(Action)

EXPL_MAX = 1.0
EXPL_MIN = 0.05
EXPL_DECAY = 0.96


class NeuralFittedStrategy2(BlackjackStrategy):
    # Some of the following code was adapted from:
    #   Hands-on Machine Learning with Scikit-Learn, Keras & TensorFlow
    #     O'Reilly, ch18 - https://homl.info/
    _experience_buffer = deque(maxlen=1000)
    _exploration_rate = EXPL_MAX
    _model = Sequential([
        Dense(24, activation='elu', input_shape=[num_inputs]),
        Dense(24, activation='elu'),
        Dense(num_outputs)
    ])
    _model.summary()

    def __init__(self, batch_size=50):
        self._batch_size = batch_size
        if len(NeuralFittedStrategy2._experience_buffer) >= self._batch_size:
            self._experience_replay()

    def evaluate(self, game_state: BlackjackState) -> Action:
        if random() < NeuralFittedStrategy2._exploration_rate:
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
        NeuralFittedStrategy2._experience_buffer.append((experience, reward))

    def _experience_replay(self, discount_factor=0.95, optimizer=Nadam(learning_rate=1e-2), loss_fn=mean_squared_error):
        if len(NeuralFittedStrategy2._experience_buffer) < self._batch_size:
            print(f"Not enough experiences to sample a batch size of: {self._batch_size}")
            return
        
        batch = sample(self._experience_buffer, self._batch_size)
        for exp, exp_reward in batch:
            q_update = (exp_reward + discount_factor * np.amax(NeuralFittedStrategy2._model.predict(exp.resulting_state)[0]))
            q_values = NeuralFittedStrategy2._model.predict(exp.last_state)
            q_values[0][exp.action.value] = q_update
            NeuralFittedStrategy2._model.fit(exp.last_state, q_values, verbose=0)

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