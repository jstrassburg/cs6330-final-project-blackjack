from enum import Enum


class TerminationStates(Enum):
    WON = 1000
    LOST = 1001
    BUST = 1002
    PUSH = 1003
