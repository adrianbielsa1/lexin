from enum import auto, IntEnum, unique

# Values are important here so we can prioritize.
@unique
class State(IntEnum):
    REJECT  = 0
    MAYBE   = 1
    ACCEPT  = 2

# Determines whether "actual" string is or can be the "expected" string.
def _compare(actual: str, expected: str):
    # Small cache.
    actual_length   = len(actual)
    expected_length = len(expected)

    if actual_length < expected_length:
        if actual == expected[0 : actual_length]:
            return State.MAYBE
        else:
            return State.REJECT
    elif actual_length == expected_length:
        if actual == expected:
            return State.ACCEPT
        else:
            return State.REJECT
    else:
        return State.REJECT

