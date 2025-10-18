from typing import List, Self, Sequence, Type

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
    def __init__(self: Self) -> None:
        super().__init__(b"\r")

    def __repr__(self: Self) -> str:
        return "\\r"


class LineFeed(Bytes):
    def __init__(self: Self) -> None:
        super().__init__(b"\n")

    def __repr__(self: Self) -> str:
        return "\\n"


class FormFeed(Ctrl):
    def __init__(self: Self) -> None:
        super().__init__("L")

    def __repr__(self: Self) -> str:
        return "FormFeed()"


class Backspace(Ctrl):
    def __init__(self: Self) -> None:
        super().__init__("H")

    def __repr__(self: Self) -> str:
        return "Backspace()"


class Tab(Bytes):
    def __init__(self: Self) -> None:
        super().__init__(b"\t")

    def __repr__(self: Self) -> str:
        return "\\t"


CR = CarriageReturn()
LF = LineFeed()
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


def encode_tab_stops(stops: Sequence[int]) -> bytes:
    tab_stops: List[int] = list(stops)
    tab_stops.sort()

    encoded: bytes = b""

    for stop in tab_stops:
        encoded += bytes(f"{number(stop, 3)},", encoding="ascii")

    encoded = encoded[:-1] + b"."

    return encoded


class SetManyTabs(Bytes):
    def __init__(self: Self, stops: List[int]) -> None:
        self._stops = stops
        super().__init__(esc("(") + encode_tab_stops(stops))

    def __repr__(self: Self) -> str:
        return f"SetManyTabs({self._stops})"


class SetOneTab(Bytes):
    def __init__(self: Self, stop: int) -> None:
        self._stop = stop
        super().__init__(esc("U") + number(stop, 3))

    def __repr__(self: Self) -> str:
        return f"SetOneTab({self._stop})"


class ClearManyTabs(Bytes):
    def __init__(self: Self, stops: List[int]) -> None:
        self._stops = stops
        super().__init__(esc(")") + encode_tab_stops(stops))

    def __repr__(self: Self) -> str:
        return f"ClearManyTabs({self._stops})"


class ClearAllTabs(Esc):
    def __init__(self: Self) -> None:
        super().__init__("0")

    def __repr__(self: Self) -> str:
        return "ClearAllTabs()"


class TabStopEncoder:
    """
    Tab stops, as per page 65 of the ImageWriter II Technical Reference Manual.
    """

    def set_many(self: Self, stops: Sequence[int]) -> Command:
        """
        Set multiple tab stops, as per page 65 of the ImageWriter II Technical
        Reference Manual.
        """

        return SetManyTabs(list(stops))

    def set_one(self: Self, stop: int) -> Command:
        """
        Set a single tab stop, as per page 65 of the ImageWriter II Technical
        Reference Manual.
        """

        return SetOneTab(stop)

    def clear_many(self: Self, stops: Sequence[int]) -> Command:
        """
        Clear multiple tab stops, as per page 65 of the ImageWriter II
        Technical Reference Manual.
        """

        return ClearManyTabs(list(stops))

    def clear_all(self: Self) -> Command:
        """
        Clear all tab stops, as per page 65 of the ImageWriter II Technical
        Reference Manual.
        """

        return ClearAllTabs()

    def reset(self: Self, stops: Sequence[int]) -> List[Command]:
        """
        Clear and then set stops, effectively resetting them.

        As per page 68 of the ImageWriter II Technical Reference Manual, if
        the pitch is changed, the tab stops remain in their existing locations
        and no longer correspond to character column positions. Therefore,
        when changing the pitch, it is recommended to reset tab positions.
        """

        return [self.clear_all(), self.set_many(stops)]


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


class FeedMany(Bytes):
    def __init__(self: Self, lines: int) -> None:
        self._lines = lines
        super().__init__(
            ctrl("_")
            + bytes(
                {10: ":", 11: ";", 12: "<", 13: "=", 14: ">", 15: "?"}.get(
                    lines, str(lines)
                ),
                encoding="ascii",
            )
        )

    def __repr__(self: Self) -> str:
        return f"FeedMany({self._lines})"


class SetLinesPerInch(Esc):
    def __init__(self: Self, lines: LinesPerInch) -> None:
        self._lines = lines
        code = "A" if lines == 6 else "B"
        super().__init__(code)

    def __repr__(self: Self) -> str:
        return f"SetLinesPerInch({self._lines})"


class SetDistanceBetweenLines(Bytes):
    def __init__(self: Self, distance: int) -> None:
        self._distance: int = distance

        super().__init__(esc("T") + number(distance, 2))

    def __repr__(self: Self) -> str:
        return f"SetDistanceBetweenLines({self._distance})"


class LineFeedForward(Esc):
    def __init__(self: Self) -> None:
        super().__init__("f")

    def __repr__(self: Self) -> str:
        return "LineFeedForward()"


class LineFeedReverse(Esc):
    def __init__(self: Self) -> None:
        super().__init__("r")

    def __repr__(self: Self) -> str:
        return "LineFeedReverse()"


class SetAutoLFAfterCR(SetSoftwareSwitches):

    def __init__(self: Self, enabled: bool) -> None:
        self._enabled = enabled
        super().__init__(enabled, {SoftwareSwitch.AUTO_LF_AFTER_CR})

    def __repr__(self: Self) -> str:
        packed = self.pack()
        return f"SetAutoLFAfterCr({self._enabled}, {packed[0]:b} {packed[1]:b})"


class SetLFWhenLineFull(SetSoftwareSwitches):

    def __init__(self: Self, enabled: bool) -> None:
        self._enabled = enabled
        super().__init__(enabled, {SoftwareSwitch.LF_WHEN_LINE_FULL})

    def __repr__(self: Self) -> str:
        packed = self.pack()
        return f"SetLFWhenLineFull({self._enabled}, {packed[0]:b} {packed[1]:b})"


class LineFeedEncoder:
    @classmethod
    def feed(cls: Type[Self], lines: int = 1) -> Command:
        """
        Feed paper from 1 to 15 lines, as per page 70 of the ImageWriter II
        Technical Reference Manual.
        """

        assert 1 <= lines <= 15, "Must feed between 1 and 15 lines"

        if lines == 1:
            return LF

        return FeedMany(lines)

    @classmethod
    def set_lines_per_inch(cls: Type[Self], lines: LinesPerInch) -> Command:
        """
        Set lines per inch to either 6 or 8, as per page 71 of the ImageWriter
        II Technical Reference Manual.
        """

        assert lines == 6 or lines == 8, "May only set 6 or 8 lines per inch"

        return SetLinesPerInch(lines)

    @classmethod
    def set_distance_between_lines(cls: Type[Self], distance: Length) -> Command:
        """
        Set the distance between lines, as per page 71 of the ImageWriter II
        Technical Reference Manual.
        """

        dist: int = length_to_int(distance, lambda d: d.vertical)

        return SetDistanceBetweenLines(dist)

    @classmethod
    def forward(cls: Type[Self]) -> Command:
        """
        Set lines to feed forward (the default) as per page 71 of the
        ImageWriter II Technical Reference Manual.
        """

        return LineFeedForward()

    @classmethod
    def reverse(cls: Type[Self]) -> Command:
        """
        Set lines to feed in reverse as per page 71 of the ImageWriter II
        Technical Reference Manual.
        """

        return LineFeedReverse()

    @classmethod
    def set_auto_after_cr(cls: Type[Self], enabled: bool) -> Command:
        """
        Enable or disable an automatic LF after a CR, as per page 34 of the
        ImageWriter II Technical Reference Manual.
        """

        return SetAutoLFAfterCR(enabled)

    @classmethod
    def set_auto_when_line_full(cls: Type[Self], enabled: bool) -> Command:
        """
        Configure the automatic insertion of a line feed when the line is full,
        as per page 34 of the ImageWriter II Technical Reference Manual.
        """

        return SetLFWhenLineFull(enabled)


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
