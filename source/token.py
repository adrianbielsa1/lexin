# NOTE: It isn't possible to use dataclasses here since the "dataclasses" module ends up
# importing from a module called "token" which creates a circular dependency (this module has
# the same name).
from enum   import auto, Enum, unique

class Token:

    def __init__(self, kind, lexeme):
        self.kind       = kind
        self.lexeme     = lexeme

@unique
class Kind(Enum):
    # Miscellaneous.
    OPERATOR            = auto(),
    NUMBER              = auto(),
    IDENTIFIER          = auto(),
    LITERAL             = auto(),

    # Keywords.
    IF                  = auto(), # si
    THEN                = auto(), # entonces
    ELSE                = auto(), # sino
    WHILE               = auto(), # mientras
    DO                  = auto(), # hacer
    PRINT               = auto(), # mostrar

    # Symbols.
    COMMA               = auto(), # ,
    SEMICOLON           = auto(), # ;
    ASSIGNMENT          = auto(), # :=
    BRACKET_OPEN        = auto(), # [
    BRACKET_CLOSE       = auto(), # ]
    PARENTHESIS_OPEN    = auto(), # (
    PARENTHESIS_CLOSE   = auto(), # )
