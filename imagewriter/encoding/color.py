from enum import Enum
from typing import Self

from imagewriter.encoding.base import Bytes, Command, esc


class Color(Enum):
    BLACK = "0"
    YELLOW = "1"
    MAGENTA = "2"
    CYAN = "3"
    ORANGE = "4"
    RED = "ORANGE"
    GREEN = "5"
    PURPLE = "6"
    BLUE = "PURPLE"

    @property
    def code(self: Self) -> str:
        value = self.value

        try:
            return Color[value].value
        except KeyError:
            return value

    def set(self: Self) -> Command:
        return Bytes(esc("K") + self.code.encode(encoding="ascii"))
