from random import Random, choice, sample
import random

from sklearn.multioutput import MultiOutputRegressor
from blackjack.Filters import legal_move_filter
from blackjack.States import TerminationStates
from blackjack.Strategies import BlackjackExperience, BlackjackStrategy, BlackjackState
from blackjack.Cards import Card
from blackjack.Policy import Action
from sklearn.ensemble import RandomForestRegressor
from collections import deque
import numpy as np

MEM_SIZE = 1000
GAMMA = 0.95
EXPL_MAX = 1.0
EXPL_MIN = 0.05
EXPL_DECAY = 0.96


class TreeBasedStrategy(BlackjackStrategy):
    # static members
    _experience_buffer = deque(maxlen=MEM_SIZE)
    _is_fit = False
    _exploration_rate = EXPL_MAX

    def __init__(self, batch_size=20):
        self._batch_size = batch_size
        self._model = MultiOutputRegressor(RandomForestRegressor())
        self._experience_replay()

    # "act"
    def evaluate(self, game_state: BlackjackState) -> Action:
        if random() < TreeBasedStrategy._exploration_rate:
            return choice(legal_move_filter(game_state))
        else:
            legal_actions = legal_move_filter(game_state)
            inputs = game_state.to_array()
            q_values = self._model.predict(inputs)
            sorted_recommended_actions = np.argsort(q_values[0])
            best_legal_action = [
                x for x in sorted_recommended_actions if x in legal_actions][-1]
            return Action(best_legal_action)

    # "remember"
    def update_policy(self, experience: BlackjackExperience):
        reward = self.determine_reward(
            experience.last_state.hand_state, experience.bet)
        TreeBasedStrategy._experience_buffer.append((experience, reward))

    def _experience_replay(self):
        if len(TreeBasedStrategy._experience_buffer < self._batch_size):
            return
        batch = sample(TreeBasedStrategy._experience_buffer,
                       len(TreeBasedStrategy._experience_buffer))
        X = []
        targets = []
        for exp, exp_reward in TreeBasedStrategy._experience_buffer:
            if TreeBasedStrategy._is_fit:
                # predict probabilites of each action from the model
                prediction = self._model.predict(
                    exp.resulting_state.to_array())[0]
                # calcuate the reward plus discounted Q value from the highest-valued Q
                q_update = (exp_reward + GAMMA * np.max(prediction))
            else:
                # if not fit, just use the raw reward
                q_update = exp_reward

            if TreeBasedStrategy._is_fit:
                q_values = self._model.predict(exp.last_state.to_array())
            else:
                q_values = np.array([[0, 0, 0]])

            q_values[0][exp.action] = q_update
            X.append(exp.last_state.to_array())
            targets.append(q_values[0])
        
        self._model.fit(X, targets)

        TreeBasedStrategy._exploration_rate = max(
            TreeBasedStrategy._exploration_rate * EXPL_DECAY, EXPL_MIN)

    @staticmethod
    def determine_reward(hand_state, bet: int):
        if hand_state == TerminationStates.WON:
            return bet
        if hand_state in [TerminationStates.LOST, TerminationStates.BUST]:
            return -bet
        if hand_state == TerminationStates.PUSH:
            return bet / 2
        return hand_state
