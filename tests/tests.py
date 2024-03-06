import sys
sys.path.append("/home/tkinaba/Documents/Github/py/tknotes")
import unittest

from tknotes.tokenizer import tokens
from tknotes.tokenizer import htmltokenizer
from tknotes.errors import errors

class ParserTests(unittest.TestCase):
    def test_single_char_id(self):
        h = htmltokenizer.HtmlTokenizer(source="<h>")
        toks = h.readTokens()
        shouldBe = list()
        shouldBe.append(tokens.Token(tokens.TokenType.LANGLEBRACKET, "<"))
        shouldBe.append(tokens.Token(tokens.TokenType.IDENTIFIER, "h"))
        shouldBe.append(tokens.Token(tokens.TokenType.RANGLEBRACKET, ">"))
        shouldBe.append(tokens.Token(tokens.TokenType.EOF, ""))
        self.assertListEqual(toks, shouldBe)

    def test_char_list(self):
        h = htmltokenizer.HtmlTokenizer(source="<hijk>")
        toks = h.readTokens()
        shouldBe = list()
        shouldBe.append(tokens.Token(tokens.TokenType.LANGLEBRACKET, "<"))
        shouldBe.append(tokens.Token(tokens.TokenType.IDENTIFIER, "hijk"))
        shouldBe.append(tokens.Token(tokens.TokenType.RANGLEBRACKET, ">"))
        shouldBe.append(tokens.Token(tokens.TokenType.EOF, ""))
        self.assertListEqual(toks, shouldBe)

    def test_string(self):
        h = htmltokenizer.HtmlTokenizer(source="<h1>hello world</h1>")
        toks = h.readTokens()
        shouldBe = list()
        shouldBe.append(tokens.Token(tokens.TokenType.LANGLEBRACKET, "<"))
        shouldBe.append(tokens.Token(tokens.TokenType.H1, "h1"))
        shouldBe.append(tokens.Token(tokens.TokenType.RANGLEBRACKET, ">"))
        shouldBe.append(tokens.Token(tokens.TokenType.STRING, "hello world"))
        shouldBe.append(tokens.Token(tokens.TokenType.LANGLEBRACKET, "<"))
        shouldBe.append(tokens.Token(tokens.TokenType.SLASH, "/"))
        shouldBe.append(tokens.Token(tokens.TokenType.H1, "h1"))
        shouldBe.append(tokens.Token(tokens.TokenType.RANGLEBRACKET, ">"))
        shouldBe.append(tokens.Token(tokens.TokenType.EOF, ""))
        self.assertListEqual(toks, shouldBe)

    # Test string with angle bracket
    def test_string_with_ab(self):
        h = htmltokenizer.HtmlTokenizer(source="<h1>hello < world</h1>")
        toks = h.readTokens()
        shouldBe = list()
        shouldBe.append(tokens.Token(tokens.TokenType.LANGLEBRACKET, "<"))
        shouldBe.append(tokens.Token(tokens.TokenType.H1, "h1"))
        shouldBe.append(tokens.Token(tokens.TokenType.RANGLEBRACKET, ">"))
        shouldBe.append(tokens.Token(tokens.TokenType.STRING, "hello < world"))
        shouldBe.append(tokens.Token(tokens.TokenType.LANGLEBRACKET, "<"))
        shouldBe.append(tokens.Token(tokens.TokenType.SLASH, "/"))
        shouldBe.append(tokens.Token(tokens.TokenType.H1, "h1"))
        shouldBe.append(tokens.Token(tokens.TokenType.RANGLEBRACKET, ">"))
        shouldBe.append(tokens.Token(tokens.TokenType.EOF, ""))
        self.assertListEqual(toks, shouldBe)

    def test_should_raise(self):
        h = htmltokenizer.HtmlTokenizer(source="<!>")
        self.assertRaises(errors.UnexpectedCharError, h.readTokens)
