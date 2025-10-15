from typing import Self

from imagewriter.encoding.base import Command, esc, number
from imagewriter.encoding.motion import LineFeed
from imagewriter.encoding.units import Point


class PrintGraphicsData(Command):
    """
    Print graphics data, as per page 105 of the ImageWriter II Technical
    Reference Manual.
    """

    def __init__(self: Self, data: bytes) -> None:
        self._data: bytes = data

    def __bytes__(self: Self) -> bytes:
        length: int = len(self._data)
        encoded: bytes = b""

        if length % 8 == 0:
            encoded = esc("g") + number(length // 8, 3)
        else:
            encoded = esc("G") + number(length, 4)

        encoded += self._data

        return encoded


def set_graphics_distance_between_lines() -> Command:
    """
    Set the distance between lines such that two adjacent graphics lines are
    flush with each other, given the pitch.

    See page 112 of the ImageWriter II Technical Reference Manual for more
    details.
    """

    return LineFeed.set_distance_between_lines(Point(1))
