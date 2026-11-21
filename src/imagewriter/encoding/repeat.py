from typing import Self

from imagewriter.encoding.base import Bytes, esc, number


class Repeat(Bytes):
    """
    Repeat a character n times, as per page 83 of the ImageWriter II Technical
    Reference Manual.
    """

    def __init__(self: Self, character: str, n: int) -> None:
        self.character = character
        self.n = n

        super().__init__(esc("R") + number(n, 3) + character.encode(encoding="ascii"))
