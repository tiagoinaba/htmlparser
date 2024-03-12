import tkinter as tk
from tkinter import font
from tknotes.tokenizer.htmltokenizer import HtmlTokenizer
from tknotes.parser.htmlparser import HtmlParser

#root = tk.Tk()
#root.title("tknotes")
#root.configure(bg="white")
#
#font = font.Font(root, font=("JetBrains Mono", 28, "bold"))
#
#frm = tk.Frame(root, padx=10, pady=10, bg="white")
#frm.grid()
#
#for token in tokens:
#    tk.Label(frm, text=token.literal, background="white", font=font).grid()
#
#root.mainloop()
#h = HtmlTokenizer(source="<h1>hello world</h1>")
h = HtmlTokenizer(source="<h1>Hello <h2>world</h2> hehe</h1>")
tokens = h.readTokens()
p = HtmlParser(tokens)
tree = p.buildTree()
print(tree)
