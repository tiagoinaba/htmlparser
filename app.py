import tkinter as tk
from tkinter import END, Entry, Frame, Label, font
from typing import Any, Dict, Literal

from tknotes.parser.htmlparser import HtmlNode
from tknotes.tokenizer.tokens import TokenType

availableFonts = Literal["h1", "h2", "h3", "p"]
tokenTypeToFont: Dict[TokenType, availableFonts] = { 
                                                    TokenType.H1: "h1",
                                                    TokenType.H2: "h2",
                                                    TokenType.H3: "h3",
                                                    TokenType.P: "p",
                                                    }
availableProps = Literal["background", "color"]

defaultStyles = { "readonlybackground": "white", "foreground": "black" }
propDict = {
        "background": "readonlybackground",
        "color": "foreground"
        }

class App(object):
    fonts: Dict[availableFonts, font.Font]
    currentNode: HtmlNode

    def __init__(self, tree: HtmlNode):
        self.root = tk.Tk()
        self.root.title("tknotes")
        self.root.configure(bg="white", padx=30, pady=30)

        self.currentNode = tree

        self.fonts = {}
        self.fonts["h1"] = font.Font(self.root, font=("JetBrains Mono", 28, "bold"))
        self.fonts["h2"] = font.Font(self.root, font=("JetBrains Mono", 24, "bold"))
        self.fonts["h3"] = font.Font(self.root, font=("JetBrains Mono", 20, "bold"))
        self.fonts["p"] = font.Font(self.root, font=("JetBrains Mono", 16))

        self.readTree(tree)

        self.root.mainloop()

    def tokenTypeToFont(self, tokenType: TokenType):
        return self.fonts[tokenTypeToFont[tokenType]]

    def readTree(self, parent: HtmlNode, styles: Dict = dict(defaultStyles)):
        for prop in parent.props:
            styles[propDict[prop.key]] = prop.value
        for node in parent.children:
            if node.type == TokenType.STRING:
                e = Entry(self.root, cursor="arrow", borderwidth=0, highlightthickness=0,  font=self.tokenTypeToFont(parent.type), **styles)
                e.insert(END, node.innerText)
                e.pack(fill="x")
                e.configure(state="readonly")
            else:
                self.readTree(node, dict(styles))
