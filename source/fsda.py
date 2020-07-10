from enum import auto, IntEnum, unique

# Values are important here so we can prioritize.
@unique
class State(IntEnum):
    REJECT = 0
    MAYBE = 1
    ACCEPT = 2

# Determines whether "actual" string is or can be the "expected" string.
def _compare(actual: str, expected: str):
    # Small cache.
    actual_length = len(actual)
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

def operator(lexeme):
    best_state = State.REJECT

    for f in [operator_additive, operator_relational, operator_multiplicative]:
        best_state = max(best_state, f(lexeme))

    return best_state

def operator_additive(lexeme):
    best_state = State.REJECT

    for expected in ["+", "-", "or"]:
        best_state = max(best_state, _compare(lexeme, expected))

        if best_state == State.ACCEPT:
            break

    return best_state

def operator_relational(lexeme):
    best_state = State.REJECT

    for expected in ["==", ">=", "<=", "!=", ">", "<"]:
        best_state = max(best_state, _compare(lexeme, expected))

        if best_state == State.ACCEPT:
            break

    return best_state

def operator_multiplicative(lexeme):
    best_state = State.REJECT

    for expected in ["*", "/", "mod", "and"]:
        best_state = max(best_state, _compare(lexeme, expected))

        if best_state == State.ACCEPT:
            break

    return best_state

def number(lexeme):
    dots = 0

    # The first character cannot be a dot.
    if lexeme[0] == ".":
        return State.REJECT

    for i, c in enumerate(lexeme):
        if c == ".":
            dots += 1

            if dots > 1:
                return State.REJECT
        elif not c.isdigit():
            return State.REJECT

    # If the last character is a dot then the number is not complete.
    if c == ".":
        return State.MAYBE
    else:
        return State.ACCEPT

def identifier(lexeme):
    if not lexeme[0].isalpha():
        return State.REJECT

    for c in lexeme[1:]:
        if (not c.isalpha()) and (not c.isdigit()):
            return State.REJECT

    return State.ACCEPT

def literal(lexeme):
    leading = lexeme.startswith("'")
    trailing = lexeme.endswith("'")
    count = lexeme.count("'")

    if count == 1:
        if leading:
            return State.MAYBE
        else:
            return State.REJECT
    elif count == 2:
        if leading and trailing:
            return State.ACCEPT
        else:
            return State.REJECT
    else:
        return State.REJECT

def keyword_if(lexeme):
    return _compare(lexeme, "si")

def keyword_then(lexeme):
    return _compare(lexeme, "entonces")

def keyword_else(lexeme):
    return _compare(lexeme, "sino")

def keyword_while(lexeme):
    return _compare(lexeme, "mientras")

def keyword_do(lexeme):
    return _compare(lexeme, "hacer")

def keyword_print(lexeme):
    return _compare(lexeme, "mostrar")

def comma(lexeme):
    return _compare(lexeme, ",")

def semicolon(lexeme):
    return _compare(lexeme, ";")

def assignment(lexeme):
    return _compare(lexeme, ":=")

def bracket_open(lexeme):
    return _compare(lexeme, "[")

def bracket_close(lexeme):
    return _compare(lexeme, "]")

def parenthesis_open(lexeme):
    return _compare(lexeme, "(")

def parenthesis_close(lexeme):
    return _compare(lexeme, ")")
