from __future__ import annotations
from typing import List
from htmlparser.tokenizer.tokens import TokenType, tokDict, Token, closingTags
from htmlparser.parser.prop import Prop
from htmlparser.errors.parser_error import ExpectedValueError

class HtmlNode(object):
    type: TokenType
    props: List[Prop]
    innerText: str
    children: List[HtmlNode]

    def __init__(self, type: TokenType, innerText: str = ""):
        self.type = type
        self.children = []
        self.props = []
        self.innerText = innerText

    def __eq__(self, other) -> bool:
        if isinstance(other, HtmlNode):
            return self.type == other.type \
                    and self.innerText == other.innerText \
                    and self.children == other.children \
                    and self.props == other.props
        return False

    def __repr__(self) -> str:
        if self.type == TokenType.STRING:
            return "HtmlNode{" + tokDict[self.type] \
                    + ", innerText='" + self.innerText \
                    + "'}"
        else:
            return "HtmlNode{" + tokDict[self.type] \
                    + ", children=" + self.children.__repr__() + ", props=" + \
                    self.props.__repr__() + "}"

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
                if self.currentToken.type == TokenType.PROP:
                    prop = Prop(key=self.currentToken.literal)
                    if self.peek().type != TokenType.EQ:
                        prop.value = "True"
                    else:
                        self.advance()
                        if self.peek().type != TokenType.VALUE:
                            raise ExpectedValueError("Expected value after prop")
                        self.advance()
                        prop.setValue(self.currentToken.literal.strip('"'))
                        currentNode.props.append(prop)
                        self.advance()
                    continue
                self.readNode(currentNode)
                continue
            else:
                currentNode.children.append(HtmlNode(self.currentToken.type, self.currentToken.literal))
            self.advance()
        self.advance()

    def addNode(self, parentNode: HtmlNode, node: HtmlNode):
        parentNode.children.append(node)

    def peek(self) -> Token:
        return self.tokens[self.current + 1]

    def advance(self):
        if self.current < len(self.tokens) - 1:
            self.current += 1
            self.currentToken = self.tokens[self.current]

