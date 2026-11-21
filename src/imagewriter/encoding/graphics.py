from typing import Self

from imagewriter.base.units import Point
from imagewriter.encoding.base import Command, esc, number
from imagewriter.encoding.motion import SetDistanceBetweenLines


class PrintGraphicsData(Command):
    """
    Print graphics data, as per page 105 of the ImageWriter II Technical
    Reference Manual.
    """

    def __init__(self: Self, data: bytes) -> None:
        self._data: bytes = data

    def __len__(self: Self) -> int:
        return len(self._data)

    @property
    def _uint64(self: Self) -> bool:
        # Whether or not data is packed into 64 bit chunks
        return len(self) % 8 == 0

    @property
    def _number_bytes(self: Self) -> bytes:
        return number(len(self), 4)

    @property
    def _number_uint64(self: Self) -> bytes:
        return number(len(self) // 8, 3)

    def __bytes__(self: Self) -> bytes:
        encoded: bytes = b""

        if self._uint64:
            encoded = esc("g") + self._number_uint64
        else:
            encoded = esc("G") + self._number_bytes

        encoded += self._data

        return encoded

    def __repr__(self: Self) -> str:
        data = " ".join([bin(byte) for byte in self._data])
        return f"PrintGraphicsData({data})"


# Set the distance between lines such that two adjacent graphics lines are
# flush with each other, given the pitch.

# See page 112 of the ImageWriter II Technical Reference Manual for more
# details.
SET_GRAPHICS_DISTANCE_BETWEEN_LINES = SetDistanceBetweenLines(Point(1))
