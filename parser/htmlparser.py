from typing import List
from tknotes.tokenizer.tokens import TokenType, tokDict, Token, closingTags

class HtmlNode(object):
    type: TokenType
    innerText: str
    def __init__(self, type: TokenType, innerText: str = ""):
        self.type = type
        self.children = []
        self.innerText = innerText

    def __eq__(self, other) -> bool:
        if isinstance(other, HtmlNode):
            return self.type == other.type and self.innerText == other.innerText and self.children == other.children
        return False

    def __repr__(self) -> str:
        if self.type == TokenType.STRING:
            return "HtmlNode{" + tokDict[self.type] \
                    + ", innerText='" + self.innerText \
                    + "'}"
        else:
            return "HtmlNode{" + tokDict[self.type] \
                    + ", children=" + self.children.__repr__() + "}"

class HtmlParser(object):
    tokens: List[Token]
    rootNode: HtmlNode
    current: int
    currentToken: Token

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = -1
        self.currentToken = Token(TokenType.ROOT, '')
        self.advance()
        pass

    def buildTree(self) -> HtmlNode:
        self.rootNode = HtmlNode(TokenType.ROOT)
        while self.currentToken.type != TokenType.EOF and self.current < len(self.tokens) - 1:
            self.readNode(self.rootNode)
        return self.rootNode

    def readNode(self, parent: HtmlNode):
        currentNode = HtmlNode(self.currentToken.type, self.currentToken.literal)
        self.addNode(parent, currentNode)
        self.advance()
        while self.currentToken.type != TokenType.EOF and self.currentToken.type != closingTags[currentNode.type]:
            if self.currentToken.type != TokenType.STRING:
                self.readNode(currentNode)
                continue
            else:
                currentNode.children.append(HtmlNode(self.currentToken.type, self.currentToken.literal))
            self.advance()
        self.advance()

    def addNode(self, parentNode: HtmlNode, node: HtmlNode):
        parentNode.children.append(node)

    def advance(self):
        if self.current < len(self.tokens) - 1:
            self.current += 1
            self.currentToken = self.tokens[self.current]

