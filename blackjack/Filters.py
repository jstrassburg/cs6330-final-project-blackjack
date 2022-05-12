from blackjack.Strategies import BlackjackState, TerminationStates
from blackjack.Policy import Action


def legal_move_filter(game_state: BlackjackState, double_any_two_cards=False):
    if game_state.hand_state in TerminationStates:
        return [Action.STAND]
    if game_state.hand_state in [10, 11] or double_any_two_cards:
        return [Action.STAND, Action.HIT, Action.DOUBLE_DOWN]
    return [Action.STAND, Action.HIT]
