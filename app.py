import tkinter as tk
from tkinter import END, Text, font
from typing import Dict, Literal

from htmlparser.parser.parser import HtmlNode
from htmlparser.tokenizer.tokens import TokenType, tokDict

availableFonts = Literal["h1", "h2", "h3", "p"]
tokenTypeToFont: Dict[TokenType, availableFonts] = { 
                                                    TokenType.H1: "h1",
                                                    TokenType.H2: "h2",
                                                    TokenType.H3: "h3",
                                                    TokenType.P: "p",
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
        self.root.configure(bg="white", padx=30, pady=30)

        self.currentNode = tree

        self.fonts = {}
        self.fonts["h1"] = font.Font(self.root, font=("JetBrains Mono", 28, "bold"))
        self.fonts["h2"] = font.Font(self.root, font=("JetBrains Mono", 24, "bold"))
        self.fonts["h3"] = font.Font(self.root, font=("JetBrains Mono", 20, "bold"))
        self.fonts["p"] = font.Font(self.root, font=("JetBrains Mono", 16))

        self.t = Text(self.root, cursor="arrow", wrap='word', borderwidth=0, highlightthickness=0, background="white")

        self.readTree(tree)

        self.t.tag_configure("<h1>", font=self.fonts["h1"])
        self.t.tag_configure("<h2>", font=self.fonts["h2"])
        self.t.tag_configure("<h3>", font=self.fonts["h3"])
        self.t.tag_configure("<p>", font=self.fonts["p"])
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
                tags.append(tokDict[parent.type])
                self.t.insert(END, node.innerText + '\n', tags)
                self.t.pack(fill="both")
            else:
                self.readTree(node, list(tags))
