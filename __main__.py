from tknotes.tokenizer.htmltokenizer import HtmlTokenizer
from tknotes.parser.htmlparser import HtmlParser
from tknotes.app import App

h = HtmlTokenizer(source="""
                            <h1 background="red" color="white">
                                testetestestetstes
                                aaaaaaaaaaaaaa
                                teste
                                oi eu sou o kiyoshi
                            </h1>
                            <h2>world</h2>
                            <p>
                                testetestestetstes
                            </p>
                            """)
tokens = h.readTokens()
p = HtmlParser(tokens)
tree = p.buildTree()

app = App(tree)
