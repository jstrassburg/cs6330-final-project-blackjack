from random import random, choice, sample
from sklearn.exceptions import NotFittedError

from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import OneHotEncoder
from blackjack.Filters import legal_move_filter
from blackjack.States import TerminationStates
from blackjack.Strategies import BlackjackExperience, BlackjackStrategy, BlackjackState
from blackjack.Cards import Card, Face, Suit
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
    _model = MultiOutputRegressor(RandomForestRegressor())
    _hand_state_encoder = OneHotEncoder(categories=[list(range(1,22)) + list([x.value for x in TerminationStates])], sparse=False)
    _dealer_show_card_encoder = OneHotEncoder(categories=[list(range(2,12))], sparse=False)

    def __init__(self, batch_size=20):
        self._batch_size = batch_size
        self._experience_replay()

    # "act"
    def evaluate(self, game_state: BlackjackState) -> Action:
        if random() < TreeBasedStrategy._exploration_rate:
            return Action(choice(legal_move_filter(game_state)))
        else:
            legal_actions = legal_move_filter(game_state)
            inputs = self.preprocess_state(game_state)
            q_values = TreeBasedStrategy._model.predict([inputs])
            sorted_recommended_actions = np.argsort(q_values[0])
            best_legal_action = [
                x for x in sorted_recommended_actions if x in legal_actions][-1]
            return Action(best_legal_action)

    # "remember"
    def update_policy(self, experience: BlackjackExperience):
        reward = self.determine_reward(
            experience.resulting_state.hand_state, experience.bet)
        TreeBasedStrategy._experience_buffer.append((experience, reward))

    def _experience_replay(self):
        if len(TreeBasedStrategy._experience_buffer) < self._batch_size:
            return
        X = []
        targets = []
        for exp, exp_reward in TreeBasedStrategy._experience_buffer:
            # predict probabilites of each action from the model
            inputs = self.preprocess_state(exp.resulting_state)
            try:
                prediction = TreeBasedStrategy._model.predict([inputs])[0]
            except NotFittedError:
                prediction = np.array([[0, 0, 0]])

            # calcuate the reward plus discounted Q value from the highest-valued Q
            q_update = (exp_reward + GAMMA * np.max(prediction))

            inputs = self.preprocess_state(exp.last_state)
            try:
                q_values = TreeBasedStrategy._model.predict([inputs])
            except NotFittedError:
                q_values = np.array([[0, 0, 0]])

            q_values[0][exp.action.value] = q_update
            inputs = self.preprocess_state(exp.last_state)
            X.append(inputs)
            targets.append(q_values[0])
        
        TreeBasedStrategy._model.fit(X, targets)

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

    @staticmethod
    def preprocess_state(state: BlackjackState):
        hand_state_encoded = TreeBasedStrategy._hand_state_encoder.fit_transform(np.array([int(state.hand_state)]).reshape(-1,1))
        dealer_show_card_encoded = TreeBasedStrategy._dealer_show_card_encoder.fit_transform(np.array([int(state.dealer_show_card)]).reshape(-1,1))
        return np.concatenate([hand_state_encoded[0], dealer_show_card_encoded[0], np.array([int(state.is_soft_hand)])])

    @staticmethod
    def print_policy():
        for i in range(1,22):
            for j in list(Face):
                for k in [True, False]:
                    state = BlackjackState(i, k, Card(j, Suit.Clubs))
                    inputs = TreeBasedStrategy.preprocess_state(state)
                    q_values = TreeBasedStrategy._model.predict([inputs])
                    sorted_recommended_actions = np.argsort(q_values[0])
                    legal_actions = legal_move_filter(state)
                    best_legal_action = [
                        x for x in sorted_recommended_actions if x in legal_actions][-1]
                    print(f"Player: {i} - Dealer: {j} - Action: {Action(best_legal_action)}")
