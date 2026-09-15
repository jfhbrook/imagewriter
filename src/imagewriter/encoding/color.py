from typing import Self

from imagewriter.color import Color
from imagewriter.encoding.base import Bytes, esc


class SetColor(Bytes):
    def __init__(self: Self, color: Color) -> None:
        self.color = color
        super().__init__(esc("K") + color.code.encode(encoding="ascii"))

    def __repr__(self: Self) -> str:
        return f"SetColor({self.color})"
