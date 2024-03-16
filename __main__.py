from tokenizer.htmltokenizer import HtmlTokenizer
from parser.htmlparser import HtmlParser
from app import App

h = HtmlTokenizer(source="""
                            <h1 background="red" color="white">
                                h1
                                <p>teste</p>
                            </h1>
                            <h2>h2</h2>
                            <h3>h3</h3>
                            <p>
                                p
                            </p>
                            """)
tokens = h.readTokens()
p = HtmlParser(tokens)
tree = p.buildTree()

app = App(tree)
