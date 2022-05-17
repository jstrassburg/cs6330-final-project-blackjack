from enum import Enum


class TerminationStates(Enum):
    WON = 22
    LOST = 23
    BUST = 24
    PUSH = 25

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    def __int__(self):
        return self.value

    def __float__(self):
        return float(self.value)
