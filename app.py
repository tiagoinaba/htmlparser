import tkinter as tk
from tkinter import INSERT, font
from tkinter.constants import CENTER
from typing import Dict, Literal

from htmlparser.parser.parser import HtmlNode
from htmlparser.tokenizer.tokens import TokenType, tokDict
from htmlparser.widgets.DynamicText import DynamicText

from widgets.ScrollingFrame import ScrollingFrame

availableFonts = Literal["h1", "h2", "h3", "p", "code"]
tokenTypeToFont: Dict[TokenType, availableFonts] = { 
                                                    TokenType.H1: "h1",
                                                    TokenType.H2: "h2",
                                                    TokenType.H3: "h3",
                                                    TokenType.P: "p",
                                                    TokenType.CODE: "code",
                                                    }
availableProps = Literal["background", "color"]

defaultStyles = { "background": "white", "foreground": "black" }
propDict = {
        "background": "background",
        "color": "foreground"
        }

tagDict = {
        "background": "bg-",
        "color": "text-"
        }

class App(object):
    fonts: Dict[availableFonts, font.Font]
    currentNode: HtmlNode

    def __init__(self, tree: HtmlNode):
        self.root = tk.Tk()
        self.root.title("tknotes")

        self.currentNode = tree

        self.fonts = {}
        self.fonts["h1"] = font.Font(self.root, font=("FreeSerif", 28, "bold"))
        self.fonts["h2"] = font.Font(self.root, font=("FreeSerif", 24, "bold"))
        self.fonts["h3"] = font.Font(self.root, font=("FreeSerif", 20, "bold"))
        self.fonts["p"] = font.Font(self.root, font=("FreeSerif", 16))
        self.fonts["code"] = font.Font(self.root, font=("JetBrains Mono", 16))

        self.main_frame = ScrollingFrame(self.root)
        self.t = DynamicText(self.main_frame, cursor="arrow", wrap='word', \
                    borderwidth=0, highlightthickness=0, background="white", padx=30, pady=30)

        self.t.tag_configure("pad", font=self.fonts["h1"])
        self.t.tag_configure("<h1>", font=self.fonts["h1"], justify=CENTER)
        self.t.tag_configure("<h2>", font=self.fonts["h2"])
        self.t.tag_configure("<h3>", font=self.fonts["h3"])
        self.t.tag_configure("<p>", font=self.fonts["p"], spacing2=0)
        self.t.tag_configure("ROOT", font=self.fonts["p"], spacing2=0)
        self.t.tag_configure("<code>", font=self.fonts["code"], background="#D9D9C1", lmargin1=50, spacing1=0, spacing2=5, spacing3=0)

        self.t.pack(side="top", fill="both", expand=True)
        self.root.update_idletasks()

        self.readTree(tree)

        self.t.configure(state="disabled")

        self.root.mainloop()

    def tokenTypeToFont(self, tokenType: TokenType):
        return self.fonts[tokenTypeToFont[tokenType]]

    def readTree(self, parent: HtmlNode, tags = []):
        for prop in parent.props:
            tag = tagDict[prop.key] + prop.value
            tagStyle = {
                    propDict[prop.key]: prop.value
                    }
            self.t.tag_configure(tag, **tagStyle)
            tags.append(tag)
        for node in parent.children:
            if node.type == TokenType.STRING:
                tags.append(tokDict.get(parent.type, "<p>"))
                self.t.insert(INSERT, node.innerText + '\n', tags)
            else:
                self.readTree(node, list(tags))
