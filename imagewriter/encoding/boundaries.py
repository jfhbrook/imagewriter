from typing import Self

from imagewriter.encoding.base import esc, number, Packet
from imagewriter.encoding.pitch import Pitch
from imagewriter.encoding.units import Length, length_to_int


class SetLeftMargin(Packet):
    """
    Set the left margin, as per page 59 of the ImageWriter II Technical
    Reference Manual.
    """

    def __init__(self: Self, width: Length, pitch: Pitch) -> None:
        self._width: Length = width
        self.pitch: Pitch = pitch

    @property
    def width(self: Self) -> int:
        """
        The margin width as an int.
        """

        return length_to_int(self._width, lambda w: w.characters(self.pitch))

    @width.setter
    def width(self: Self, width: Length) -> None:
        """
        Set the margin width as an int or Unit.
        """

        self._width = width

    def data(self: Self) -> bytes:
        return esc("L") + number(self.width, 3)


class SetPageLength(Packet):
    """
    Set the page length, as per page 61 of the ImageWriter II Technical
    Reference Manual.
    """

    def __init__(self: Self, length: Length) -> None:
        self._length: Length = length

    @property
    def length(self: Self) -> int:
        """
        The page length as an int.
        """

        return length_to_int(self.length, lambda lg: lg.vertical)

    @length.setter
    def length(self: Self, length: Length) -> None:
        """
        Set the page length, either as an int or a Unit.
        """

        self._length = length

    def data(self: Self) -> bytes:
        return esc("H") + number(self.length, 4)
