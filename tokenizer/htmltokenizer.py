from tknotes.tokenizer.tokens import TokenType, tokDict, Token
from tknotes.errors.errors import UnexpectedCharError
from typing import List

class HtmlTokenizer(object):
    source: str
    char: str
    currentIndex: int
    nextIndex: int
    tokens: List[Token]
    inBrackets: bool

    def __init__(self, source) -> None:
        self.source = source
        self.currentIndex = -1
        self.nextIndex = 0
        self.tokens = []
        self.inBrackets = False
        self.advance()

    def readTokens(self) -> List[Token]:
        while self.char != '':
            self.tokens.append(self.readToken())
        self.tokens.append(Token(TokenType.EOF, ''))
        return self.tokens

    def readToken(self) -> Token:
        tok = None
        match self.char:
            case "<":
                self.inBrackets = True
                tok = Token(TokenType.LANGLEBRACKET, self.source[self.currentIndex:self.nextIndex])
            case ">":
                self.inBrackets = False
                tok = Token(TokenType.RANGLEBRACKET, self.source[self.currentIndex:self.nextIndex])
            case "/":
                tok = Token(TokenType.SLASH, self.source[self.currentIndex:self.nextIndex])
            case _:
                if not self.inBrackets:
                    tok = self.readString()
                    return tok
                if self.char.isalpha():
                    # Early return so we don't call self.advance() twice
                    tok = self.readIdentifier()
                    return tok
                else:
                    raise UnexpectedCharError("Unexpected char '{char}'".format(char=self.char))
        self.advance()
        return tok

    def readIdentifier(self) -> Token:
        start = self.currentIndex
        while self.char.isalnum():
            self.advance()
        literal = self.source[start:self.currentIndex]
        try:
            type = list(tokDict.keys())[list(tokDict.values()).index(literal)]
        except:
            type = TokenType.IDENTIFIER
        return Token(type, literal)

    def readString(self, start = -1) -> Token:
        if start < 0:
            start = self.currentIndex
        while self.char != '<':
            self.advance()
        if self.peek() == '/':
            return Token(TokenType.STRING, self.source[start:self.currentIndex])
        else:
            self.advance()
            return self.readString(start)

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
            self.char = ''
