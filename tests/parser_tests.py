import unittest

from htmlparser.tokenizer.htmltokenizer import HtmlTokenizer
from htmlparser.tokenizer.htmltokenizer import TokenType
from htmlparser.parser.parser import HtmlNode, HtmlParser
from htmlparser.parser.prop import Prop

from htmlparser.errors.parser_error import UnknownPropError

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
        self.assertEqual(root, shouldBe)

    def test_props(self):
        h = HtmlTokenizer(source="<h1 color=\"white\">Hello <h2>world</h2> hehe</h1>")
        toks = h.readTokens()
        p = HtmlParser(toks)
        root = p.buildTree()
        shouldBe = HtmlNode(TokenType.ROOT, "")
        h1 = HtmlNode(TokenType.H1, "<h1 ")
        h1.props.append(Prop("color", "white"))
        h1.children.append(HtmlNode(TokenType.STRING, "Hello "))
        h2 = HtmlNode(TokenType.H2, "<h2>")
        h1.children.append(h2)
        h2.children.append(HtmlNode(TokenType.STRING, "world"))
        h1.children.append(HtmlNode(TokenType.STRING, " hehe"))
        shouldBe.children.append(h1)
        self.assertEqual(root, shouldBe)

    def test_props_nested(self):
        h = HtmlTokenizer(source="<h1 color=\"white\">Hello <h2 color=\"red\">world</h2> hehe</h1>")
        toks = h.readTokens()
        p = HtmlParser(toks)
        root = p.buildTree()
        shouldBe = HtmlNode(TokenType.ROOT, "")
        h1 = HtmlNode(TokenType.H1, "<h1 ")
        h1.props.append(Prop("color", "white"))
        h1.children.append(HtmlNode(TokenType.STRING, "Hello "))
        h2 = HtmlNode(TokenType.H2, "<h2 ")
        h1.children.append(h2)
        h2.children.append(HtmlNode(TokenType.STRING, "world"))
        h2.props.append(Prop("color", "red"))
        h1.children.append(HtmlNode(TokenType.STRING, " hehe"))
        shouldBe.children.append(h1)
        self.assertEqual(root, shouldBe)

    def test_unknown_prop_error(self):
        h = HtmlTokenizer(source="<h1 balls=\"2\">Hello <h2>world</h2> hehe</h1>")
        toks = h.readTokens()
        p = HtmlParser(toks)
        self.assertRaises(UnknownPropError, p.buildTree)

    def test_unknown_prop_value_error(self):
        h = HtmlTokenizer(source="<h1 balls=\"2\">Hello <h2>world</h2> hehe</h1>")
        toks = h.readTokens()
        p = HtmlParser(toks)
        self.assertRaises(UnknownPropError, p.buildTree)

    def test_code_tag(self):
        h = HtmlTokenizer(source="""
<code>
    def teste(param):
        print("hello world")
</code>
                                        """)
        toks = h.readTokens()
        p = HtmlParser(toks)
        tree = p.buildTree()
        shouldBe = HtmlNode(TokenType.ROOT)
        code = HtmlNode(TokenType.CODE, "<code>")
        code.children.append(HtmlNode(TokenType.STRING, """
    def teste(param):
        print("hello world")
"""))
        shouldBe.children.append(code)
        self.assertEqual(tree, shouldBe)
