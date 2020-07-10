import dataclasses
import enum
import fsda
import typing

@enum.unique
class TokenKind(enum.Enum):
    # Miscellaneous.
    OPERATOR = enum.auto(), # ==, >, <, >=, <=, !=, *, /, mod, and, +, -, or
    NUMBER = enum.auto(),
    IDENTIFIER = enum.auto(),
    LITERAL = enum.auto(),

    # Keywords.
    IF = enum.auto(), # si
    THEN = enum.auto(), # entonces
    ELSE = enum.auto(), # sino
    WHILE = enum.auto(), # mientras
    DO = enum.auto(), # hacer
    PRINT = enum.auto(), # mostrar

    # Symbols.
    COMMA = enum.auto(), # ,
    SEMICOLON = enum.auto(), # ;
    ASSIGNMENT = enum.auto(), # :=
    BRACKET_OPEN = enum.auto(), # [
    BRACKET_CLOSE = enum.auto(), # ]
    PARENTHESIS_OPEN = enum.auto(), # (
    PARENTHESIS_CLOSE = enum.auto(), # )

@dataclasses.dataclass
class Token:
    kind: TokenKind
    lexeme: str

class TokenNotRecognisedError(Exception):

    def __init__(self, lexeme):
        self.lexeme = lexeme

# Order matters here (to prioritize).
_kind_to_automaton = {
    TokenKind.IF: fsda.keyword_if,
    TokenKind.THEN: fsda.keyword_then,
    TokenKind.ELSE: fsda.keyword_else,
    TokenKind.WHILE: fsda.keyword_while,
    TokenKind.DO: fsda.keyword_do,
    TokenKind.PRINT: fsda.keyword_print,

    TokenKind.OPERATOR: fsda.operator,

    TokenKind.COMMA: fsda.comma,
    TokenKind.SEMICOLON: fsda.semicolon,
    TokenKind.ASSIGNMENT: fsda.assignment,
    TokenKind.BRACKET_OPEN: fsda.bracket_open,
    TokenKind.BRACKET_CLOSE: fsda.bracket_close,
    TokenKind.PARENTHESIS_OPEN: fsda.parenthesis_open,
    TokenKind.PARENTHESIS_CLOSE: fsda.parenthesis_close,

    TokenKind.NUMBER: fsda.number,
    TokenKind.IDENTIFIER: fsda.identifier,
    TokenKind.LITERAL: fsda.literal,
}

# Converts a stream of characters into a stream of tokens.
def tokenize(text: str) -> typing.List[Token]:
    # Resulting tokens extracted from the text.
    tokens = []

    # Add a space at the end of the text in order to make stopping easier.
    text += " "

    # Iterators used to slice the text.
    start = 0
    index = 0

    # Loop until the end.
    while index < len(text):
        if text[index : index + 1].isspace():
            index += 1
            continue

        # Move our start position forward (ignoring what we've already processed) and prepare
        # the rest of the variables for a new analysis.
        start = index

        lexeme = ""

        last_accepted_tokens = []
        next_accepted_tokens = []

        all_rejected    = False

        while True:
            # Get all the FSDA that accept this lexeme.
            lexeme = text[start : index + 1]
            next_accepted_tokens, all_rejected = _calculate_token_candidates(lexeme)

            # No FSDA can accept this lexeme now, and never will. Leave!
            if all_rejected:
                break

            # TODO: Review. Is it possible to go from accepted to maybe to rejected?
            last_accepted_tokens = next_accepted_tokens
            index += 1

        if not last_accepted_tokens:
            raise TokenNotRecognisedError(lexeme)

        # Trim the lexeme one character before every automaton rejected it and pick the most
        # relevant candidate token.
        lexeme = text[start : index]
        kind = last_accepted_tokens[0]

        tokens.append(Token(kind, lexeme))

    return tokens

def _calculate_token_candidates(lexeme: str) -> (typing.List[TokenKind], bool):
    accepting_candidates = []
    all_rejected = True

    for kind, automaton in _kind_to_automaton.items():
        state = automaton(lexeme)

        if state == fsda.State.ACCEPT:
            accepting_candidates.append(kind)

        all_rejected = all_rejected and (state == fsda.State.REJECT)

    return accepting_candidates, all_rejected
