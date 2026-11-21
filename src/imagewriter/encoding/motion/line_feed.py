from typing import Self

from imagewriter.base.motion import LinesPerInch
from imagewriter.base.units import Length, length_to_int
from imagewriter.encoding.base import (
    Bytes,
    Esc,
    LengthError,
    ctrl,
    esc,
    number,
)

LINE_FEED_ENCODING: dict[int, bytes] = {
    10: b":",
    11: b";",
    12: b"<",
    13: b"=",
    14: b">",
    15: b"?",
}

for i in range(2, 10):
    LINE_FEED_ENCODING[i] = bytes(str(i), encoding="ascii")


class LineFeedLengthError(LengthError):
    """
    An error raised when a line feed has no meaningful length.
    """


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
            super().__init__(ctrl("_") + LINE_FEED_ENCODING[lines])

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
        self.distance: int = dist

        super().__init__(esc("T") + number(dist, 2))

    def __repr__(self: Self) -> str:
        return f"SetDistanceBetweenLines({self.distance})"


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


LINE_FEED_FORWARD = LineFeedForward()
LINE_FEED_REVERSE = LineFeedReverse()
