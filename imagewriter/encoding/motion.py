from typing import List, Self, Sequence

from imagewriter.encoding.base import ctrl, esc, format_number
from imagewriter.encoding.length import Inch, Length
from imagewriter.encoding.pitch import Pitch

CR = b"\r"
LF = b"\n"
BACKSPACE = ctrl("H")
TAB = b"\t"


def set_unidirectional_printing(is_unidirectional: bool) -> bytes:
    """
    Configure unidirectional printing, as per page 63 of the ImageWriter II
    Technical Reference Manual.
    """

    if is_unidirectional:
        return esc(">")
    return esc("<")


class TabStops:
    """
    Tab stops, as per page 65 of the ImageWriter II Technical Reference Manual.

    Note that, if the character pitch changes, the tab stops remain the same.
    It is a good idea to clear and reset tab stops
    """

    def __init__(self: Self, pitch: Pitch) -> None:
        self.pitch: Pitch = pitch
        self.stops: List[Length] = list()

    def _to_int(self: Self, length: Length | int) -> int:
        stop: int = 0
        if isinstance(length, Length):
            stop = int(length.inches * self.pitch.characters_per_inch)
        else:
            stop = length

        return min(stop, self.pitch.characters_per_line - 1)

    def _to_length(self: Self, length: Length | int) -> Length:
        if isinstance(length, Length):
            return length
        return Inch(length / self.pitch.characters_per_inch)

    def _to_list(self: Self, stops: Sequence[Length | int]) -> bytes:
        tab_stops: List[int] = [self._to_int(st) for st in stops]
        tab_stops.sort()

        encoded: bytes = b""

        for stop in tab_stops:
            encoded += bytes(f"{format_number(stop, 3)},", encoding="ascii")

        encoded = encoded[:-1] + b"."

        return encoded

    def _sort_stops(self: Self) -> None:
        self.stops.sort(key=self._to_int)

    def set_many(self: Self, stops: Sequence[Length | int]) -> bytes:
        """
        Set multiple tab stops, as per page 65 of the ImageWriter II Technical
        Reference Manual.
        """

        self.stops = [self._to_length(st) for st in stops]
        self._sort_stops()

        return esc("(") + self._to_list(stops)

    def set_one(self: Self, stop: Length | int) -> bytes:
        """
        Set a single tab stop, as per page 65 of the ImageWriter II Technical
        Reference Manual.
        """

        self.stops.append(self._to_length(stop))
        self._sort_stops()

        tab_stop = self._to_int(stop)

        return esc("U", format_number(tab_stop, 3))

    def clear_many(self: Self, stops: Sequence[Length | int]) -> bytes:
        """
        Clear multiple tab stops, as per page 65 of the ImageWriter II
        Technical Reference Manual.
        """

        self.stops = [
            self._to_length(st)
            for st in (
                {self._to_int(st) for st in self.stops}
                - {self._to_int(st) for st in stops}
            )
        ]
        self._sort_stops()

        return esc(")") + self._to_list(stops)

    def clear_all(self: Self) -> bytes:
        """
        Clear all tab stops, as per page 65 of the ImageWriter II Technical
        Reference Manual.
        """

        self.stops = list()

        return esc("0")

    def set_pitch(self: Self, pitch: Pitch) -> bytes:
        """
        Set the pitch used for tab stops and reset all stored tab stops.

        As per page 68 of the ImageWriter II Technical Reference Manual, if
        the pitch is changed, the tab stops remain in their existing locations
        and no longer correspond to character column positions. Therefore,
        when changing the pitch, it is recommended to reset tab positions.
        """

        self.pitch = pitch
        return self.clear_all() + self.set_many(self.stops)


def place_exact_print_head_position(position: Length | int, pitch: Pitch) -> bytes:
    """
    Place the exact print head position, as per page 120 of the ImageWriter
    II Technical Reference Manual.

    Position is typically specified in dots per inch, based on the pitch.
    """

    pos: int = 0

    if isinstance(position, Length):
        pos = int(position.inches * pitch.horizontal_resolution)
    else:
        pos = position

    pos = min(pos, pitch.width)

    return esc("F", format_number(pos, 4))


SET_TOP_OF_FORM = esc("v")
