from re import error

class UnexpectedCharError(error):
    def __init__(self, msg: str, pattern: str | bytes | None = None, pos: int | None = None) -> None:
        super().__init__(msg, pattern, pos)

class UnclosedAngledBracket(error):
    def __init__(self, msg: str, pattern: str | bytes | None = None, pos: int | None = None) -> None:
        super().__init__(msg, pattern, pos)
