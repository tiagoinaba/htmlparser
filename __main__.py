from tknotes.tokenizer.htmltokenizer import HtmlTokenizer

h = HtmlTokenizer(source="<h1>hello world</h1>")
print(h.readTokens())
