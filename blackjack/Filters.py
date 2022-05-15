from blackjack.Strategies import BlackjackState, TerminationStates
from blackjack.Policy import Action


def legal_move_filter(game_state: BlackjackState, double_any_two_cards=False):
    if TerminationStates.has_value(game_state.hand_state):
        return [Action.STAND.value]
    if game_state.hand_state in [10, 11] or double_any_two_cards:
        return [Action.STAND.value, Action.HIT.value, Action.DOUBLE_DOWN.value]
    return [Action.STAND.value, Action.HIT.value]
