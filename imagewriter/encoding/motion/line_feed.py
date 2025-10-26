from typing import Self

from imagewriter.encoding.base import (
    Bytes,
    ctrl,
    esc,
    Esc,
    LengthError,
    number,
)
from imagewriter.motion import LinesPerInch
from imagewriter.units import Length, length_to_int


def _encode_line_feed_count(lines: int) -> bytes:
    return bytes(
        {10: ":", 11: ";", 12: "<", 13: "=", 14: ">", 15: "?"}.get(lines, str(lines)),
        encoding="ascii",
    )


class LineFeedLengthError(LengthError):
    """
    An error raised when a line feed has no meaningful length.
    """

    pass


class LineFeed(Bytes):
    """
    Feed paper from 1 to 15 lines, as per page 70 of the ImageWriter II
    Technical Reference Manual.
    """

    def __init__(self: Self, lines: int) -> None:
        assert 1 <= lines <= 15, "Must feed between 1 and 15 lines"

        self.lines = lines

        if lines == 1:
            super().__init__(b"\n")
        else:

            super().__init__(ctrl("_") + _encode_line_feed_count(lines))

    def __repr__(self: Self) -> str:
        if self.lines == 1:
            return "<LF>"

        return f"LineFeed({self.lines})"

    def __len__(self: Self) -> int:
        raise LineFeedLengthError("Line feeds do not have a meaningful length")


LF = LineFeed(1)


class SetLinesPerInch(Esc):
    """
    Set lines per inch to either 6 or 8, as per page 71 of the ImageWriter
    II Technical Reference Manual.
    """

    def __init__(self: Self, lines: LinesPerInch) -> None:
        assert lines == 6 or lines == 8, "May only set 6 or 8 lines per inch"

        self._lines = lines
        code = "A" if lines == 6 else "B"
        super().__init__(code)

    def __repr__(self: Self) -> str:
        return f"SetLinesPerInch({self._lines})"


class SetDistanceBetweenLines(Bytes):
    """
    Set the distance between lines, as per page 71 of the ImageWriter II
    Technical Reference Manual.
    """

    def __init__(self: Self, distance: Length) -> None:
        dist: int = length_to_int(distance, lambda d: d.vertical)
        self._distance: int = dist

        super().__init__(esc("T") + number(dist, 2))

    def __repr__(self: Self) -> str:
        return f"SetDistanceBetweenLines({self._distance})"


class LineFeedForward(Esc):
    """
    Set lines to feed forward (the default) as per page 71 of the
    ImageWriter II Technical Reference Manual.
    """

    def __init__(self: Self) -> None:
        super().__init__("f")

    def __repr__(self: Self) -> str:
        return "LineFeedForward()"


class LineFeedReverse(Esc):
    """
    Set lines to feed in reverse as per page 71 of the ImageWriter II
    Technical Reference Manual.
    """

    def __init__(self: Self) -> None:
        super().__init__("r")

    def __repr__(self: Self) -> str:
        return "LineFeedReverse()"
