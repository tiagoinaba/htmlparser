from htmlparser.tokenizer.htmltokenizer import HtmlTokenizer
from htmlparser.parser.parser import HtmlParser
from htmlparser.app import App

h = HtmlTokenizer(source="""
<h1>Teste</h1>
<code>
    def teste(param):
        print("hello world")
</code>
<p>hello buddy</p>
                                        """)
toks = h.readTokens()
p = HtmlParser(toks)
app = App(p.buildTree())
