import unittest
import lexer

class TestKeywords(unittest.TestCase):

    def test_if(self):
        actual = lexer.tokenize("si")
        expected = [
            lexer.Token(lexer.TokenKind.IF, "si"),
            lexer.Token(lexer.TokenKind.EOF, "EOF"),
        ]

        self.assertEqual(actual, expected)

    def test_then(self):
        actual = lexer.tokenize("entonces")
        expected = [
            lexer.Token(lexer.TokenKind.THEN, "entonces"),
            lexer.Token(lexer.TokenKind.EOF, "EOF"),
        ]

        self.assertEqual(actual, expected)

    def test_else(self):
        actual = lexer.tokenize("sino")
        expected = [
            lexer.Token(lexer.TokenKind.ELSE, "sino"),
            lexer.Token(lexer.TokenKind.EOF, "EOF"),
        ]

        self.assertEqual(actual, expected)

    def test_while(self):
        actual = lexer.tokenize("mientras")
        expected = [
            lexer.Token(lexer.TokenKind.WHILE, "mientras"),
            lexer.Token(lexer.TokenKind.EOF, "EOF"),
        ]

        self.assertEqual(actual, expected)

    def test_do(self):
        actual = lexer.tokenize("hacer")
        expected = [
            lexer.Token(lexer.TokenKind.DO, "hacer"),
            lexer.Token(lexer.TokenKind.EOF, "EOF"),
        ]

        self.assertEqual(actual, expected)

    def test_print(self):
        actual = lexer.tokenize("mostrar")
        expected = [
            lexer.Token(lexer.TokenKind.PRINT, "mostrar"),
            lexer.Token(lexer.TokenKind.EOF, "EOF"),
        ]

        self.assertEqual(actual, expected)

class TestMiscellaneous(unittest.TestCase):

    def test_valid_operators(self):
        for op in ["==", ">", "<", ">=", "<=", "!="]:
            actual = lexer.tokenize(op)
            expected = [
                lexer.Token(lexer.TokenKind.OPERATOR, op),
                lexer.Token(lexer.TokenKind.EOF, "EOF"),
            ]

            self.assertEqual(actual, expected)

    def test_invalid_operators(self):
        for op in ["$=", "%="]:
            self.assertRaises(lexer.TokenNotRecognisedError, lexer.tokenize, op)

    def test_valid_numbers(self):
        for n in ["3.14", "123", "54564345.1", "424242.23", "000"]:
            actual = lexer.tokenize(n)
            expected = [
                lexer.Token(lexer.TokenKind.NUMBER, n),
                lexer.Token(lexer.TokenKind.EOF, "EOF"),
            ]

            self.assertEqual(actual, expected)

    def test_invalid_numbers(self):
        for n in [".00", ".11", "123."]:
            self.assertRaises(lexer.TokenNotRecognisedError, lexer.tokenize, n)

    def test_valid_identifiers(self):
        for id in ["hola", "como", "va", "lolsito"]:
            actual = lexer.tokenize(id)
            expected = [
                lexer.Token(lexer.TokenKind.IDENTIFIER, id),
                lexer.Token(lexer.TokenKind.EOF, "EOF"),
            ]

            self.assertEqual(actual, expected)

    def test_invalid_identifiers(self):
        for id in ["$$$", "hol@"]:
            self.assertRaises(lexer.TokenNotRecognisedError, lexer.tokenize, id)

class TestPhrases(unittest.TestCase):

    def test_valid_phrases(self):
        valid_phrases = {
            "si aa entonces bb() sino cc()": [
                lexer.Token(lexer.TokenKind.IF, "si"),
                lexer.Token(lexer.TokenKind.IDENTIFIER, "aa"),
                lexer.Token(lexer.TokenKind.THEN, "entonces"),
                lexer.Token(lexer.TokenKind.IDENTIFIER, "bb"),
                lexer.Token(lexer.TokenKind.PARENTHESIS_OPEN, "("),
                lexer.Token(lexer.TokenKind.PARENTHESIS_CLOSE, ")"),
                lexer.Token(lexer.TokenKind.ELSE, "sino"),
                lexer.Token(lexer.TokenKind.IDENTIFIER, "cc"),
                lexer.Token(lexer.TokenKind.PARENTHESIS_OPEN, "("),
                lexer.Token(lexer.TokenKind.PARENTHESIS_CLOSE, ")"),
                lexer.Token(lexer.TokenKind.EOF, "EOF"),
            ],

            "mientras tiempoLibre hacer jugarLolsito": [
                lexer.Token(lexer.TokenKind.WHILE, "mientras"),
                lexer.Token(lexer.TokenKind.IDENTIFIER, "tiempoLibre"),
                lexer.Token(lexer.TokenKind.DO, "hacer"),
                lexer.Token(lexer.TokenKind.IDENTIFIER, "jugarLolsito"),
                lexer.Token(lexer.TokenKind.EOF, "EOF"),
            ],

            "42.43 < 45": [
                lexer.Token(lexer.TokenKind.NUMBER, "42.43"),
                lexer.Token(lexer.TokenKind.OPERATOR, "<"),
                lexer.Token(lexer.TokenKind.NUMBER, "45"),
                lexer.Token(lexer.TokenKind.EOF, "EOF"),
            ],

            "222<<>>444": [
                lexer.Token(lexer.TokenKind.NUMBER, "222"),
                lexer.Token(lexer.TokenKind.OPERATOR, "<"),
                lexer.Token(lexer.TokenKind.OPERATOR, "<"),
                lexer.Token(lexer.TokenKind.OPERATOR, ">"),
                lexer.Token(lexer.TokenKind.OPERATOR, ">"),
                lexer.Token(lexer.TokenKind.NUMBER, "444"),
                lexer.Token(lexer.TokenKind.EOF, "EOF"),
            ]
        }

        for actual, expected in valid_phrases.items():
            self.assertEqual(lexer.tokenize(actual), expected)

    def test_invalid_phrases(self):
        invalid_phrases = [
            "si @ entonces",
            "mientras 66.666. hacer a()",
        ]

        for phrase in invalid_phrases:
            self.assertRaises(lexer.TokenNotRecognisedError, lexer.tokenize, phrase)
