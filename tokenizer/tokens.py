from enum import Enum
from typing import Dict

class TokenType(Enum):
    IDENTIFIER      = 1
    EOF             = 2
    STRING          = 3
    H1              = 4
    H2              = 5
    H3              = 6
    P               = 7
    H1C             = 8
    H2C             = 9
    H3C             = 10
    PC              = 11
    ROOT            = 12

tokDict: Dict[TokenType, str] = {
    TokenType.IDENTIFIER: "IDENTIFIER",
    TokenType.EOF: "EOF",
    TokenType.STRING: "STRING",
    TokenType.H1: "<h1>",
    TokenType.H2: "<h2>",
    TokenType.H3: "<h3>",
    TokenType.P:  "<p>",
    TokenType.H1C: "</h1>",
    TokenType.H2C: "</h2>",
    TokenType.H3C: "</h3>",
    TokenType.PC:  "</p>",
    TokenType.ROOT:  "ROOT",
}

keywords: Dict[str, TokenType] = {
     "<h1>":  TokenType.H1,
     "<h2>":  TokenType.H2,
     "<h3>":  TokenType.H3,
     "<p>":   TokenType.P,
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
        
