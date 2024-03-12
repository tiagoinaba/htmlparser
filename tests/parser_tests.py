import sys
sys.path.append("/home/tkinaba/Documents/Github/py/tknotes")
import unittest

from tknotes.tokenizer.htmltokenizer import HtmlTokenizer
from tknotes.tokenizer.htmltokenizer import Token, TokenType
from tknotes.parser.htmlparser import HtmlNode, HtmlParser

class ParserTests(unittest.TestCase):
    def test_hello_world(self):
        h = HtmlTokenizer(source="<h1>Hello world</h1>")
        toks = h.readTokens()
        p = HtmlParser(toks)
        root = p.buildTree()
        shouldBe = HtmlNode(TokenType.ROOT, "")
        h1 = HtmlNode(TokenType.H1, "<h1>")
        h1.children.append(HtmlNode(TokenType.STRING, "Hello world"))
        shouldBe.children.append(h1)
        self.assertEqual(root, shouldBe)

    def test_no_tags(self):
        h = HtmlTokenizer(source="Hello world")
        toks = h.readTokens()
        p = HtmlParser(toks)
        root = p.buildTree()
        shouldBe = HtmlNode(TokenType.ROOT, "")
        shouldBe.children.append(HtmlNode(TokenType.STRING, "Hello world"))
        self.assertEqual(root, shouldBe)

    def test_nested_tags(self):
        h = HtmlTokenizer(source="<h1>Hello <h2>world</h2> hehe</h1>")
        toks = h.readTokens()
        p = HtmlParser(toks)
        root = p.buildTree()
        shouldBe = HtmlNode(TokenType.ROOT, "")
        h1 = HtmlNode(TokenType.H1, "<h1>")
        h1.children.append(HtmlNode(TokenType.STRING, "Hello "))
        h2 = HtmlNode(TokenType.H2, "<h2>")
        h1.children.append(h2)
        h2.children.append(HtmlNode(TokenType.STRING, "world"))
        h1.children.append(HtmlNode(TokenType.STRING, " hehe"))
        shouldBe.children.append(h1)
        print(root)
        print(shouldBe)
        self.assertEqual(root, shouldBe)
