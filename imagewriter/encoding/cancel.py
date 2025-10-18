from typing import Self

from imagewriter.encoding.base import Ctrl


class CancelCurrentLine(Ctrl):
    """
    When ^X is encountered anywhere in the currently buffered line, that line will
    not be printed on the next Print Command.

    See page 85 of the ImageWriter II Technical Reference Manual for more details.
    """

    def __init__(self: Self) -> None:
        super().__init__("X")

    def __repr__(self: Self) -> str:
        return "CancelCurrentLine()"


CANCEL_CURRENT_LINE = CancelCurrentLine()
