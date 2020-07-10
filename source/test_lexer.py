import unittest
import lexer

class TestKeywords(unittest.TestCase):

    def test_if(self):
        actual = lexer.tokenize("si")
        expected = [
            lexer.Token(lexer.TokenKind.IF, "si")
        ]

        self.assertEqual(actual, expected)

    def test_then(self):
        actual = lexer.tokenize("entonces")
        expected = [
            lexer.Token(lexer.TokenKind.THEN, "entonces")
        ]

        self.assertEqual(actual, expected)

    def test_else(self):
        actual = lexer.tokenize("sino")
        expected = [
            lexer.Token(lexer.TokenKind.ELSE, "sino")
        ]

        self.assertEqual(actual, expected)

    def test_while(self):
        actual = lexer.tokenize("mientras")
        expected = [
            lexer.Token(lexer.TokenKind.WHILE, "mientras")
        ]

        self.assertEqual(actual, expected)

    def test_do(self):
        actual = lexer.tokenize("hacer")
        expected = [
            lexer.Token(lexer.TokenKind.DO, "hacer")
        ]

        self.assertEqual(actual, expected)

    def test_print(self):
        actual = lexer.tokenize("mostrar")
        expected = [
            lexer.Token(lexer.TokenKind.PRINT, "mostrar")
        ]

        self.assertEqual(actual, expected)

class TestMiscellaneous(unittest.TestCase):

    def test_valid_operators(self):
        for op in ["==", ">", "<", ">=", "<=", "!="]:
            actual = lexer.tokenize(op)
            expected = [
                lexer.Token(lexer.TokenKind.OPERATOR, op)
            ]

            self.assertEqual(actual, expected)

    def test_invalid_operators(self):
        for op in ["$=", "%="]:
            self.assertRaises(lexer.TokenNotRecognisedError, lexer.tokenize, op)

    def test_valid_numbers(self):
        for n in ["3.14", "123", "54564345.1", "424242.23", "000"]:
            actual = lexer.tokenize(n)
            expected = [
                lexer.Token(lexer.TokenKind.NUMBER, n)
            ]

            self.assertEqual(actual, expected)

    def test_invalid_numbers(self):
        for n in [".00", ".11", "123."]:
            self.assertRaises(lexer.TokenNotRecognisedError, lexer.tokenize, n)

    def test_valid_identifiers(self):
        for id in ["hola", "como", "va", "lolsito"]:
            actual = lexer.tokenize(id)
            expected = [
                lexer.Token(lexer.TokenKind.IDENTIFIER, id)
            ]

            self.assertEqual(actual, expected)

    def test_invalid_identifiers(self):
        for id in ["$$$", "hol@"]:
            self.assertRaises(lexer.TokenNotRecognisedError, lexer.tokenize, id)
