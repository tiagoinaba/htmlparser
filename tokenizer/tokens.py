from enum import Enum
from typing import Dict

class TokenType(Enum):
    LANGLEBRACKET   = 1
    RANGLEBRACKET   = 2
    IDENTIFIER      = 3
    SLASH           = 4
    EOF             = 5
    STRING          = 6
    H1              = 7
    H2              = 8
    H3              = 9
    P               = 10

tokDict: Dict[TokenType, str] = {
    TokenType.LANGLEBRACKET: "LANGLEBRACKET",
    TokenType.RANGLEBRACKET: "RANGLEBRACKET",
    TokenType.IDENTIFIER: "IDENTIFIER",
    TokenType.SLASH: "SLASH",
    TokenType.EOF: "EOF",
    TokenType.STRING: "STRING",
    TokenType.H1: "h1",
    TokenType.H2: "h2",
    TokenType.H3: "h3",
    TokenType.P: "p",
}

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
        
