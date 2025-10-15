from typing import List, Literal, Self, Sequence, Type

from imagewriter.encoding.base import (
    Bytes,
    ctrl,
    Ctrl,
    esc,
    Esc,
    number,
    Packet,
)
from imagewriter.encoding.pitch import Pitch
from imagewriter.encoding.units import (
    Distance,
    Inch,
    Length,
    length_to_distance,
    length_to_int,
)

CR = Bytes(b"\r")
LF = Bytes(b"\n")
FF = Ctrl("L")
BACKSPACE = Ctrl("H")
TAB = Bytes(b"\t")


class SetUnidirectionalPrinting(Esc):
    """
    Configure unidirectional printing, as per page 63 of the ImageWriter II
    Technical Reference Manual.
    """

    def __init__(self: Self, is_unidirectional: bool) -> None:
        code = ">" if is_unidirectional else "<"
        super().__init__(code)


class TabStops:
    """
    Tab stops, as per page 65 of the ImageWriter II Technical Reference Manual.

    Note that, if the character pitch changes, the tab stops remain the same.
    It is a good idea to clear and reset tab stops
    """

    def __init__(self: Self, pitch: Pitch) -> None:
        self.pitch: Pitch = pitch
        self.stops: List[Distance] = list()

    def _to_int(self: Self, length: Length) -> int:
        stop: int = length_to_int(length, lambda lg: lg.characters(self.pitch))

        return min(stop, self.pitch.max_character_position)

    def _to_distance(self: Self, length: Length) -> Distance:
        return length_to_distance(
            length, lambda lg: Inch(lg / self.pitch.characters_per_inch)
        )

    def _to_list(self: Self, stops: Sequence[Length]) -> bytes:
        tab_stops: List[int] = [self._to_int(st) for st in stops]
        tab_stops.sort()

        encoded: bytes = b""

        for stop in tab_stops:
            encoded += bytes(f"{number(stop, 3)},", encoding="ascii")

        encoded = encoded[:-1] + b"."

        return encoded

    def _sort_stops(self: Self) -> None:
        self.stops.sort(key=self._to_int)

    def set_many(self: Self, stops: Sequence[Length]) -> Packet:
        """
        Set multiple tab stops, as per page 65 of the ImageWriter II Technical
        Reference Manual.
        """

        self.stops = [self._to_distance(st) for st in stops]
        self._sort_stops()

        return Bytes(esc("(") + self._to_list(stops))

    def set_one(self: Self, stop: Length) -> Packet:
        """
        Set a single tab stop, as per page 65 of the ImageWriter II Technical
        Reference Manual.
        """

        self.stops.append(self._to_distance(stop))
        self._sort_stops()

        tab_stop = self._to_int(stop)

        return Bytes(esc("U") + number(tab_stop, 3))

    def clear_many(self: Self, stops: Sequence[Length]) -> Packet:
        """
        Clear multiple tab stops, as per page 65 of the ImageWriter II
        Technical Reference Manual.
        """

        self.stops = [
            self._to_distance(st)
            for st in (
                {self._to_int(st) for st in self.stops}
                - {self._to_int(st) for st in stops}
            )
        ]
        self._sort_stops()

        return Bytes(esc(")") + self._to_list(stops))

    def clear_all(self: Self) -> Packet:
        """
        Clear all tab stops, as per page 65 of the ImageWriter II Technical
        Reference Manual.
        """

        self.stops = list()

        return Esc("0")

    def set_pitch(self: Self, pitch: Pitch) -> List[Packet]:
        """
        Set the pitch used for tab stops and reset all stored tab stops.

        As per page 68 of the ImageWriter II Technical Reference Manual, if
        the pitch is changed, the tab stops remain in their existing locations
        and no longer correspond to character column positions. Therefore,
        when changing the pitch, it is recommended to reset tab positions.
        """

        self.pitch = pitch
        return [self.clear_all(), self.set_many(self.stops)]


class PlaceExactPrintHeadPosition(Packet):
    """
    Place the exact print head position, as per page 120 of the ImageWriter
    II Technical Reference Manual.

    Position is typically specified in dots per inch, based on the pitch.
    """

    def __init__(self: Self, position: Length, pitch: Pitch) -> None:
        self._position: Length = position
        self.pitch: Pitch = pitch

    @property
    def position(self: Self) -> int:
        pos: int = length_to_int(self.position, lambda p: p.horizontal_dpi(self.pitch))

        return min(pos, self.pitch.width)

    @position.setter
    def position(self: Self, position: Length) -> None:
        self._position = position

    def data(self: Self) -> bytes:
        return esc("F") + number(self.position, 4)


SET_TOP_OF_FORM = Esc("v")


class LineFeed:
    @classmethod
    def feed(cls: Type[Self], lines: int = 1) -> Packet:
        """
        Feed paper from 1 to 15 lines, as per page 70 of the ImageWriter II
        Technical Reference Manual.
        """

        assert 1 <= lines <= 15, "Must feed between 1 and 15 lines"

        if lines == 1:
            return LF

        return Bytes(
            ctrl("_")
            + bytes(
                {10: ":", 11: ";", 12: "<", 13: "=", 14: ">", 15: "?"}.get(
                    lines, str(lines)
                ),
                encoding="ascii",
            )
        )

    @classmethod
    def set_lines_per_inch(cls: Type[Self], lines: Literal[6] | Literal[8]) -> Packet:
        """
        Set lines per inch to either 6 or 8, as per page 71 of the ImageWriter
        II Technical Reference Manual.
        """

        assert lines == 6 or lines == 8, "May only set 6 or 8 lines per inch"

        if lines == 6:
            return Esc("A")
        else:
            return Esc("B")

    @classmethod
    def set_distance_between_lines(cls: Type[Self], distance: Length) -> Packet:
        """
        Set the distance between lines, as per page 71 of the ImageWriter II
        Technical Reference Manual.
        """

        dist: int = length_to_int(distance, lambda d: d.vertical)

        return Bytes(esc("T") + number(dist, 2))

    @classmethod
    def forward(cls: Type[Self]) -> Packet:
        """
        Set lines to feed forward (the default) as per page 71 of the
        ImageWriter II Technical Reference Manual.
        """

        return Esc("f")

    @classmethod
    def reverse(cls: Type[Self]) -> Packet:
        """
        Set lines to feed in reverse as per page 71 of the ImageWriter II
        Technical Reference Manual.
        """

        return Esc("r")
