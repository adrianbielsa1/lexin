from enum import auto, IntEnum, unique

# Values are important here so we can prioritize.
@unique
class State(IntEnum):
    TRAP = 0
    MAYBE = 1
    ACCEPT = 2

# Determines whether "actual" string is or can be the "expected" string.
def _compare(actual: str, expected: str):
    if actual == expected:
        return State.ACCEPT
    elif len(actual) > len(expected):
        return State.TRAP
    elif actual == expected[0 : len(actual)]:
        return State.MAYBE
    else:
        return State.TRAP

def operator(lexeme):
    best_state = State.TRAP

    for f in [operator_additive, operator_relational, operator_multiplicative]:
        best_state = max(best_state, f(lexeme))

    return best_state

def operator_additive(lexeme):
    best_state = State.TRAP

    for expected in ["+", "-", "or"]:
        best_state = max(best_state, _compare(lexeme, expected))

        if best_state == State.ACCEPT:
            break

    return best_state

def operator_relational(lexeme):
    best_state = State.TRAP

    for expected in ["==", ">=", "<=", "!=", ">", "<"]:
        best_state = max(best_state, _compare(lexeme, expected))

        if best_state == State.ACCEPT:
            break

    return best_state

def operator_multiplicative(lexeme):
    best_state = State.TRAP

    for expected in ["*", "/", "mod", "and"]:
        best_state = max(best_state, _compare(lexeme, expected))

        if best_state == State.ACCEPT:
            break

    return best_state

def number(lexeme):
    dots = 0

    # The first character cannot be a dot.
    if lexeme[0] == ".":
        return State.TRAP

    for i, c in enumerate(lexeme):
        if c == ".":
            dots += 1

            if dots > 1:
                return State.TRAP
        elif not c.isdigit():
            return State.TRAP

    # If the last character is a dot then the number is not complete.
    if c == ".":
        return State.MAYBE
    else:
        return State.ACCEPT

def identifier(lexeme):
    if not lexeme[0].isalpha():
        return State.TRAP

    for c in lexeme[1:]:
        if (not c.isalpha()) and (not c.isdigit()):
            return State.TRAP

    return State.ACCEPT

def literal(lexeme):
    leading = lexeme.startswith("'")
    trailing = lexeme.endswith("'")

    for c in lexeme[1 : len(lexeme) - 1]:
        if (not c.isdigit()) and (not c.isalpha()):
            return State.TRAP

    # TODO: Maybe we can move one of those ifs above the for loop to avoid processing
    # each character if there are both no leading and trailing symbols.
    if leading and trailing:
        return State.ACCEPT
    elif leading:
        return State.MAYBE
    else:
        return State.TRAP

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
