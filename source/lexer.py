import fsda
import token
import typing

class UnrecognisedTokenError(Exception):

    def __init__(self, lexeme):
        self.lexeme = lexeme

# Order matters here (to prioritize).
_kind_to_automaton = {
    token.Kind.IF:                  fsda.keyword_if,
    token.Kind.THEN:                fsda.keyword_then,
    token.Kind.ELSE:                fsda.keyword_else,
    token.Kind.WHILE:               fsda.keyword_while,
    token.Kind.DO:                  fsda.keyword_do,
    token.Kind.PRINT:               fsda.keyword_print,

    token.Kind.OPERATOR:            fsda.operator,
    token.Kind.NUMBER:              fsda.number,
    token.Kind.IDENTIFIER:          fsda.identifier,
    token.Kind.LITERAL:             fsda.literal,

    token.Kind.COMMA:               fsda.comma,
    token.Kind.SEMICOLON:           fsda.semicolon,
    token.Kind.ASSIGNMENT:          fsda.assignment,
    token.Kind.BRACKET_OPEN:        fsda.bracket_open,
    token.Kind.BRACKET_CLOSE:       fsda.bracket_close,
    token.Kind.PARENTHESIS_OPEN:    fsda.parenthesis_open,
    token.Kind.PARENTHESIS_CLOSE:   fsda.parenthesis_close
}

# Converts a stream of characters into a stream of tokens.
def tokenize(text: str) -> typing.List[token.Token]:
    # Resulting tokens extracted from the text.
    tokens  = []

    # Add a space at the end of the text in order to make stopping easier.
    text    += " "

    # Iterators used to slice the text.
    start   = 0
    index   = 0

    # Loop until the end.
    while index < len(text):
        if text[index : index + 1].isspace():
            index += 1
            continue

        # Move our start position forward (ignoring what we've already processed) and prepare
        # the rest of the variables for a new analysis.
        start                   = index

        lexeme                  = ""

        last_accepted_tokens    = []
        next_accepted_tokens    = []

        all_rejected    = False

        while True:
            # Get all the FSDA that accept this lexeme.
            lexeme                              = text[start : index + 1]
            next_accepted_tokens, all_rejected  = _calculate_token_candidates(lexeme)

            # No FSDA can accept this lexeme now, and never will. Leave!
            if all_rejected:
                break

            # TODO: Review. Is it possible to go from accepted to maybe to rejected?
            last_accepted_tokens    = next_accepted_tokens
            index                   += 1

        if not last_accepted_tokens:
            raise UnrecognisedTokenError(lexeme)

        # Trim the lexeme one character before every automaton rejected it and pick the most
        # relevant candidate token.
        lexeme  = text[start : index]
        kind    = last_accepted_tokens[0]

        tokens.append(token.Token(kind, lexeme))

    return tokens

def _calculate_token_candidates(lexeme: str) -> (typing.List[token.Kind], bool):
    accepting_candidates    = []
    all_rejected            = True

    for kind, automaton in _kind_to_automaton.items():
        state = automaton(lexeme)

        if state == fsda.State.ACCEPT:
            accepting_candidates.append(kind)

        all_rejected = all_rejected and (state == fsda.State.REJECT)

    return accepting_candidates, all_rejected
