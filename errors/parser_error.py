
from re import error


class ExpectedValueError(error):
    def __init__(self, msg: str, pattern: str | bytes | None = None, pos: int | None = None) -> None:
        super().__init__(msg, pattern, pos)
