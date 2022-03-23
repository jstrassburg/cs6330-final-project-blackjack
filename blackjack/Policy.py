from enum import Enum


class Action(Enum):
    HIT = 1
    STAND = 2


FixedPolicy = {
    1: Action.HIT,
    2: Action.HIT,
    3: Action.HIT,
    4: Action.HIT,
    5: Action.HIT,
    6: Action.HIT,
    7: Action.HIT,
    8: Action.HIT,
    9: Action.HIT,
    10: Action.HIT,
    11: Action.HIT,
    12: Action.HIT,
    13: Action.HIT,
    14: Action.STAND,
    15: Action.STAND,
    16: Action.STAND,
    17: Action.STAND,
    18: Action.STAND,
    19: Action.STAND,
    20: Action.STAND,
    21: Action.STAND
}
