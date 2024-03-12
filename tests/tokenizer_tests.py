import sys
sys.path.append("/home/tkinaba/Documents/Github/py/tknotes")
import unittest

from tknotes.tokenizer import tokens
from tknotes.tokenizer import htmltokenizer

class ParserTests(unittest.TestCase):
    def test_single_char_id(self):
        h = htmltokenizer.HtmlTokenizer(source="<h>")
        toks = h.readTokens()
        shouldBe = list()
        shouldBe.append(tokens.Token(tokens.TokenType.STRING, "<h>"))
        shouldBe.append(tokens.Token(tokens.TokenType.EOF, ""))
        self.assertListEqual(toks, shouldBe)

    def test_char_list(self):
        h = htmltokenizer.HtmlTokenizer(source="<hijk>")
        toks = h.readTokens()
        shouldBe = list()
        shouldBe.append(tokens.Token(tokens.TokenType.STRING, "<hijk>"))
        shouldBe.append(tokens.Token(tokens.TokenType.EOF, ""))
        self.assertListEqual(toks, shouldBe)

    def test_string(self):
        h = htmltokenizer.HtmlTokenizer(source="<h1>hello world</h1>")
        toks = h.readTokens()
        shouldBe = list()
        shouldBe.append(tokens.Token(tokens.TokenType.H1, "<h1>"))
        shouldBe.append(tokens.Token(tokens.TokenType.STRING, "hello world"))
        shouldBe.append(tokens.Token(tokens.TokenType.H1C, "</h1>"))
        shouldBe.append(tokens.Token(tokens.TokenType.EOF, ""))
        self.assertListEqual(toks, shouldBe)

    # Test string with angle bracket
    def test_string_with_ab(self):
        h = htmltokenizer.HtmlTokenizer(source="<h1>hello < world</h1>")
        toks = h.readTokens()
        shouldBe = list()
        shouldBe.append(tokens.Token(tokens.TokenType.H1, "<h1>"))
        shouldBe.append(tokens.Token(tokens.TokenType.STRING, "hello < world"))
        shouldBe.append(tokens.Token(tokens.TokenType.H1C, "</h1>"))
        shouldBe.append(tokens.Token(tokens.TokenType.EOF, ""))
        self.assertListEqual(toks, shouldBe)

    def test_nested_tags(self):
        h = htmltokenizer.HtmlTokenizer(source="<h1>hello<h2>teste</h2>world</h1>")
        toks = h.readTokens()
        shouldBe = list()
        shouldBe.append(tokens.Token(tokens.TokenType.H1, "<h1>"))
        shouldBe.append(tokens.Token(tokens.TokenType.STRING, "hello"))
        shouldBe.append(tokens.Token(tokens.TokenType.H2, "<h2>"))
        shouldBe.append(tokens.Token(tokens.TokenType.STRING, "teste"))
        shouldBe.append(tokens.Token(tokens.TokenType.H2C, "</h2>"))
        shouldBe.append(tokens.Token(tokens.TokenType.STRING, "world"))
        shouldBe.append(tokens.Token(tokens.TokenType.H1C, "</h1>"))
        shouldBe.append(tokens.Token(tokens.TokenType.EOF, ""))
        self.assertListEqual(toks, shouldBe)
