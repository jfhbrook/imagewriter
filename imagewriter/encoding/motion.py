from typing import List, Self, Sequence

from imagewriter.encoding.base import (
    Bytes,
    Command,
    ctrl,
    Ctrl,
    esc,
    Esc,
    number,
)
from imagewriter.encoding.switch import SetSoftwareSwitches
from imagewriter.motion import LinesPerInch
from imagewriter.pitch import Pitch
from imagewriter.switch import SoftwareSwitch
from imagewriter.units import Length, length_to_int


class CarriageReturn(Bytes):
    """
    A carriage return (\\r).
    """

    def __init__(self: Self) -> None:
        super().__init__(b"\r")

    def __repr__(self: Self) -> str:
        return "\\r"


def _encode_line_feed_count(lines: int) -> bytes:
    return bytes(
        {10: ":", 11: ";", 12: "<", 13: "=", 14: ">", 15: "?"}.get(lines, str(lines)),
        encoding="ascii",
    )


class LineFeed(Bytes):
    """
    Feed paper from 1 to 15 lines, as per page 70 of the ImageWriter II
    Technical Reference Manual.
    """

    def __init__(self: Self, lines: int) -> None:
        assert 1 <= lines <= 15, "Must feed between 1 and 15 lines"

        self._lines = lines

        if lines == 1:
            super().__init__(b"\n")
        else:

            super().__init__(ctrl("_") + _encode_line_feed_count(lines))

    def __repr__(self: Self) -> str:
        if self._lines == 1:
            return "\\n"

        return f"LineFeed({self._lines})"


class FormFeed(Ctrl):
    """
    A form feed. When encountered, feeds the paper up to a new sheet.
    """

    def __init__(self: Self) -> None:
        super().__init__("L")

    def __repr__(self: Self) -> str:
        return "FormFeed()"


class Backspace(Ctrl):
    """
    A backspace.
    """

    def __init__(self: Self) -> None:
        super().__init__("H")

    def __repr__(self: Self) -> str:
        return "Backspace()"


class Tab(Bytes):
    """
    A tab character (\\t).
    """

    def __init__(self: Self) -> None:
        super().__init__(b"\t")

    def __repr__(self: Self) -> str:
        return "\\t"


CR = CarriageReturn()
LF = LineFeed(1)
FF = FormFeed()
BACKSPACE = Backspace()
TAB = Tab()


class SetUnidirectionalPrinting(Esc):
    """
    Configure unidirectional printing, as per page 63 of the ImageWriter II
    Technical Reference Manual.
    """

    def __init__(self: Self, is_unidirectional: bool) -> None:
        self.is_unidirectional = is_unidirectional
        code = ">" if is_unidirectional else "<"
        super().__init__(code)

    def __repr__(self: Self) -> str:
        return f"SetUnidirectionalPrinting(is_unidirectional={self.is_unidirectional})"


def _encode_tab_stops(stops: Sequence[int]) -> bytes:
    tab_stops: List[int] = list(stops)
    tab_stops.sort()

    encoded: bytes = b""

    for stop in tab_stops:
        encoded += bytes(f"{number(stop, 3)},", encoding="ascii")

    encoded = encoded[:-1] + b"."

    return encoded


class SetManyTabs(Bytes):
    """
    Set multiple tab stops, as per page 65 of the ImageWriter II Technical
    Reference Manual.
    """

    def __init__(self: Self, stops: List[int]) -> None:
        self._stops = stops
        super().__init__(esc("(") + _encode_tab_stops(stops))

    def __repr__(self: Self) -> str:
        return f"SetManyTabs({self._stops})"


class SetOneTab(Bytes):
    """
    Set a single tab stop, as per page 65 of the ImageWriter II Technical
    Reference Manual.
    """

    def __init__(self: Self, stop: int) -> None:
        self._stop = stop
        super().__init__(esc("U") + number(stop, 3))

    def __repr__(self: Self) -> str:
        return f"SetOneTab({self._stop})"


class ClearManyTabs(Bytes):
    """
    Clear multiple tab stops, as per page 65 of the ImageWriter II
    Technical Reference Manual.
    """

    def __init__(self: Self, stops: List[int]) -> None:
        self._stops = stops
        super().__init__(esc(")") + _encode_tab_stops(stops))

    def __repr__(self: Self) -> str:
        return f"ClearManyTabs({self._stops})"


class ClearAllTabs(Esc):
    """
    Clear all tab stops, as per page 65 of the ImageWriter II Technical
    Reference Manual.
    """

    def __init__(self: Self) -> None:
        super().__init__("0")

    def __repr__(self: Self) -> str:
        return "ClearAllTabs()"


def reset_tabs(stops: List[int]) -> List[Command]:
    """
    Clear and then set stops, effectively resetting them.

    As per page 68 of the ImageWriter II Technical Reference Manual, if
    the pitch is changed, the tab stops remain in their existing locations
    and no longer correspond to character column positions. Therefore,
    when changing the pitch, it is recommended to reset tab positions.
    """

    clear_all: Command = ClearAllTabs()
    set_many: Command = SetManyTabs(stops)

    return [clear_all, set_many]


class PlaceExactPrintHeadPosition(Command):
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

    def __bytes__(self: Self) -> bytes:
        return esc("F") + number(self.position, 4)

    def __repr__(self: Self) -> str:
        return f"PlaceExactPrintHeadPosition({self.position})"


class SetTopOfForm(Esc):
    def __init__(self: Self) -> None:
        super().__init__("v")

    def __repr__(self: Self) -> str:
        return "SetTopOfForm()"


SET_TOP_OF_FORM = SetTopOfForm()


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


class SetAutoLFAfterCR(SetSoftwareSwitches):
    """
    Enable or disable an automatic LF after a CR, as per page 34 of the
    ImageWriter II Technical Reference Manual.
    """

    def __init__(self: Self, enabled: bool) -> None:
        self._enabled = enabled
        super().__init__(enabled, {SoftwareSwitch.AUTO_LF_AFTER_CR})

    def __repr__(self: Self) -> str:
        packed = self.pack()
        return f"SetAutoLFAfterCr({self._enabled}, {packed[0]:b} {packed[1]:b})"


class SetLFWhenLineFull(SetSoftwareSwitches):
    """
    Configure the automatic insertion of a line feed when the line is full,
    as per page 34 of the ImageWriter II Technical Reference Manual.
    """

    def __init__(self: Self, enabled: bool) -> None:
        self._enabled = enabled
        super().__init__(enabled, {SoftwareSwitch.LF_WHEN_LINE_FULL})

    def __repr__(self: Self) -> str:
        packed = self.pack()
        return f"SetLFWhenLineFull({self._enabled}, {packed[0]:b} {packed[1]:b})"


class SetPerforationSkip(SetSoftwareSwitches):
    """
    Configure automatic perforation skip, as per page 34 of the ImageWriter II
    Technical Reference Manual.
    """

    def __init__(self: Self, enabled: bool) -> None:
        self._enabled = enabled
        super().__init__(not enabled, {SoftwareSwitch.PERFORATION_SKIP_DISABLED})

    def __repr__(self: Self) -> str:
        packed = self.pack()
        return f"SetPerforationSkip({self._enabled}, {packed[0]:b} {packed[1]:b})"
