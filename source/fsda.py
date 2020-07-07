from enum import auto, IntEnum, unique

# Values are important here so we can prioritize.
@unique
class State(IntEnum):
    REJECT  = 0
    MAYBE   = 1
    ACCEPT  = 2

