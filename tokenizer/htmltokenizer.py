from tknotes.tokenizer.tokens import TokenType, getTokenType, Token
from typing import List

class HtmlTokenizer(object):
    source: str
    char: str
    currentIndex: int
    nextIndex: int
    tokens: List[Token]

    def __init__(self, source) -> None:
        self.source = source
        self.currentIndex = -1
        self.nextIndex = 0
        self.tokens = []
        self.advance()

    def readTokens(self) -> List[Token]:
        while self.char != '':
            tok = self.readToken()
            if len(self.tokens) > 0 and tok.type == TokenType.STRING and self.tokens[-1].type == TokenType.STRING:
                self.tokens[-1].literal += tok.literal
                continue
            self.tokens.append(tok)
        self.tokens.append(Token(TokenType.EOF, ''))
        return self.tokens

    def readToken(self) -> Token:
        tok = None
        match self.char:
            case "<":
                tok = self.readTag()
            case _:
                tok = self.readString()
        return tok

    def readTag(self) -> Token:
        start = self.currentIndex
        self.advance()
        while self.char != '' and self.char != '>' and self.char != '<':
            self.advance()
        if self.char == '<':
            return Token(TokenType.STRING, self.source[start:self.currentIndex])
        if self.char == '':
            return self.readString(start)
        self.advance()
        literal = self.source[start:self.currentIndex]
        return Token(getTokenType(literal), literal)

    def readString(self, start = -1) -> Token:
        if start < 0:
            start = self.currentIndex
        while self.char != '<' and self.char != '':
            self.advance()
        return Token(TokenType.STRING, self.source[start:self.currentIndex])

    def peek(self) -> str:
        if self.nextIndex < len(self.source):
            return self.source[self.nextIndex]
        else:
            return ''

    def advance(self) -> None:
        if self.currentIndex < len(self.source) - 1:
            self.currentIndex += 1
            self.nextIndex += 1
            self.char = self.source[self.currentIndex]
        else:
            self.currentIndex += 1
            self.nextIndex += 1
            self.char = ''
