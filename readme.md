# LEXIN
A small lexicographic analyzer written in Python, which takes a stream of characters as input and produces a stream of tokens as output.
## HOW TO USE
Simply import the project,
```
import lexin.lexer

tokens = lexin.lexer.tokenize("some string you want to tokenize 123")
```
Alternatively, you may also check the unit tests in the [source](source/) folder, or run them
from the command line interface using
```
python -m unittest
```
which discovers them on its own.
## ABOUT
This project was made by Adrián Bielsa (me), Lucio Calosso Cístola and Tomás Sanchez. It was brought to us by our college's "Syntax and semantics of languages" course's laboratory.
