from enum import Enum, auto
from typing import Dict

class TokenType(Enum):
    IDENTIFIER      = auto()
    EOF             = auto()
    STRING          = auto()
    VALUE           = auto()
    H1              = auto()
    H2              = auto()
    H3              = auto()
    P               = auto()
    H1C             = auto()
    H2C             = auto()
    H3C             = auto()
    PC              = auto()
    PROP            = auto()
    EQ              = auto()
    ROOT            = auto()

tokDict: Dict[TokenType, str] = {
    TokenType.IDENTIFIER: "IDENTIFIER",
    TokenType.EOF: "EOF",
    TokenType.STRING: "STRING",
    TokenType.VALUE: "VALUE",
    TokenType.H1: "<h1>",
    TokenType.H2: "<h2>",
    TokenType.H3: "<h3>",
    TokenType.P:  "<p>",
    TokenType.H1C: "</h1>",
    TokenType.H2C: "</h2>",
    TokenType.H3C: "</h3>",
    TokenType.PC:  "</p>",
    TokenType.PROP:  "PROP",
    TokenType.ROOT:  "ROOT",
    TokenType.EQ:  "EQ",
}

keywords: Dict[str, TokenType] = {
     "<h1>":  TokenType.H1,
     "<h1 ":  TokenType.H1,
     "<h2>":  TokenType.H2,
     "<h2 ":  TokenType.H2,
     "<h3>":  TokenType.H3,
     "<h3 ":  TokenType.H3,
     "<p>":   TokenType.P,
     "<p ":   TokenType.P,
     "</h1>": TokenType.H1C,
     "</h2>": TokenType.H2C,
     "</h3>": TokenType.H3C,
     "</p>":  TokenType.PC,
}

closingTags: Dict[TokenType, TokenType] = {
        TokenType.H1: TokenType.H1C,
        TokenType.H2: TokenType.H2C,
        TokenType.H3: TokenType.H3C,
        TokenType.P: TokenType.PC,
        TokenType.ROOT: TokenType.EOF,
        }

def getTokenType(literal: str) -> TokenType:
    return keywords.get(literal, TokenType.STRING)

class Token(object):
    type: TokenType
    literal: str

    def __init__(self, type, literal) -> None:
        self.type = type
        self.literal = literal

    def __str__(self) -> str:
        return "Token{" + tokDict[self.type] + ", '" + self.literal + "'}"

    def __repr__(self) -> str:
        return "Token{" + tokDict[self.type] + ", '" + self.literal + "'}"

    def __eq__(self, other) -> bool:
        return self.type == other.type and self.literal == other.literal
        
