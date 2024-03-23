from htmlparser.tokenizer.tokens import TokenType, getTokenType, Token
from htmlparser.errors.errors import UnclosedAngledBracket, UnexpectedCharError
from typing import List

class HtmlTokenizer(object):
    source: str
    char: str
    currentIndex: int
    nextIndex: int
    inBrackets: bool
    tokens: List[Token]
    shouldEatWhitespace: bool

    def __init__(self, source: str) -> None:
        self.source = source.strip()
        self.currentIndex = -1
        self.nextIndex = 0
        self.tokens = []
        self.inBrackets = False
        self.advance()
        self.shouldEatWhitespace = True

    def readTokens(self) -> List[Token]:
        while self.char != '':
            tok = self.readToken()
            if tok.type == TokenType.STRING:
                if len(tok.literal) == 0:
                    continue
                if len(self.tokens) > 0 and self.tokens[-1].type == TokenType.STRING:
                    self.tokens[-1].literal += tok.literal
                    continue
            self.tokens.append(tok)
        self.tokens.append(Token(TokenType.EOF, ''))
        return self.tokens

    def readToken(self) -> Token:
        tok = None
        match (self.char, self.shouldEatWhitespace):
            case ("\n" | "\t", True):
                self.eatWhitespace()
                tok = self.readToken()
            case ("<", _):
                if self.peek() in ("\n", "\t", " "):
                    self.advance()
                    self.eatWhitespace()
                    self.retreat()
                self.inBrackets = True
                tok = self.readTag()
                if tok.type == TokenType.CODE:
                    self.shouldEatWhitespace = False
                elif tok.type == TokenType.CODEC:
                    self.shouldEatWhitespace = True
            case (_, _):
                if self.inBrackets:
                    if self.char == ' ':
                        self.eatWhitespace()
                    tok = self.readProp()
                else:
                    tok = self.readString()
        return tok

    def readProp(self) -> Token:
        tok = None
        match self.char:
            case '=':
                tok = Token(TokenType.EQ, self.char)
                self.advance()
            case '"':
                start = self.currentIndex
                self.advance()
                while self.char != '"':
                    self.advance()
                self.advance()
                tok = Token(TokenType.VALUE, self.source[start:self.currentIndex])
            case _:
                start = self.currentIndex
                while self.char != '=':
                    self.advance()
                tok = Token(TokenType.PROP, self.source[start:self.currentIndex])
        if self.char == '>':
            self.inBrackets = False
            self.advance()
        return tok

    def readTag(self) -> Token:
        start = self.currentIndex
        self.advance()
        while self.char not in ('', '>', '<', ' '):
            self.advance()
        if self.char == '<':
            raise UnexpectedCharError("Unexpected char '" + self.source[start:self.currentIndex + 1] + "'")
        if self.char == '':
            raise UnclosedAngledBracket("Unclosed angled bracket at '" + self.source[start:self.currentIndex + 1] + "'")
        if self.char == '>':
            self.inBrackets = False
        self.advance()
        literal = self.source[start:self.currentIndex]
        return Token(getTokenType(literal), literal)

    def readString(self, start = -1) -> Token:
        if start < 0:
            start = self.currentIndex
        while self.char != '<' and self.char != '':
            self.advance()
            if self.shouldEatWhitespace and self.char in ("\n", "\t"):
                end = self.currentIndex
                self.eatWhitespace()
                return Token(TokenType.STRING, self.source[start:end] + " ")
        return Token(TokenType.STRING, self.source[start:self.currentIndex])

    def eatWhitespace(self):
        while self.char in ("\n", "\r", "\t", " "):
            self.source = self.source[:self.currentIndex] + self.source[self.currentIndex + 1:]
            self.char = self.source[self.currentIndex]

    def peek(self) -> str:
        if self.nextIndex < len(self.source):
            return self.source[self.nextIndex]
        else:
            return ''
    def retreat(self) -> None:
        if self.currentIndex > 0:
            self.currentIndex -= 1
            self.nextIndex -= 1
            self.char = self.source[self.currentIndex]

    def advance(self) -> None:
        if self.currentIndex < len(self.source) - 1:
            self.currentIndex += 1
            self.nextIndex += 1
            self.char = self.source[self.currentIndex]
        else:
            self.currentIndex += 1
            self.nextIndex += 1
            self.char = ''
