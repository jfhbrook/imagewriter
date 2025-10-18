import dataclasses
from typing import List, Self, Sequence, Tuple, Type

from imagewriter.encoding.base import (
    Bytes,
    Command,
    ctrl,
    Ctrl,
    esc,
    Esc,
    number,
)
from imagewriter.encoding.switch import (
    CloseSoftwareSwitches,
    OpenSoftwareSwitches,
    SoftwareSwitches,
)
from imagewriter.motion import LinesPerInch
from imagewriter.pitch import Pitch
from imagewriter.switch import SoftwareSwitch
from imagewriter.units import Length, length_to_int

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


class TabStopEncoder:
    """
    Tab stops, as per page 65 of the ImageWriter II Technical Reference Manual.

    Note that, if the character pitch changes, the tab stops remain the same.
    It is a good idea to clear and reset tab stops
    """

    def _to_list(self: Self, stops: Sequence[int]) -> bytes:
        tab_stops: List[int] = list(stops)
        tab_stops.sort()

        encoded: bytes = b""

        for stop in tab_stops:
            encoded += bytes(f"{number(stop, 3)},", encoding="ascii")

        encoded = encoded[:-1] + b"."

        return encoded

    def set_many(self: Self, stops: Sequence[int]) -> Command:
        """
        Set multiple tab stops, as per page 65 of the ImageWriter II Technical
        Reference Manual.
        """

        return Bytes(esc("(") + self._to_list(stops))

    def set_one(self: Self, stop: int) -> Command:
        """
        Set a single tab stop, as per page 65 of the ImageWriter II Technical
        Reference Manual.
        """

        return Bytes(esc("U") + number(stop, 3))

    def clear_many(self: Self, stops: Sequence[int]) -> Command:
        """
        Clear multiple tab stops, as per page 65 of the ImageWriter II
        Technical Reference Manual.
        """

        return Bytes(esc(")") + self._to_list(stops))

    def clear_all(self: Self) -> Command:
        """
        Clear all tab stops, as per page 65 of the ImageWriter II Technical
        Reference Manual.
        """

        return Esc("0")

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


SET_TOP_OF_FORM = Esc("v")


class LineFeed:
    @classmethod
    def feed(cls: Type[Self], lines: int = 1) -> Command:
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
    def set_lines_per_inch(cls: Type[Self], lines: LinesPerInch) -> Command:
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
    def set_distance_between_lines(cls: Type[Self], distance: Length) -> Command:
        """
        Set the distance between lines, as per page 71 of the ImageWriter II
        Technical Reference Manual.
        """

        dist: int = length_to_int(distance, lambda d: d.vertical)

        return Bytes(esc("T") + number(dist, 2))

    @classmethod
    def forward(cls: Type[Self]) -> Command:
        """
        Set lines to feed forward (the default) as per page 71 of the
        ImageWriter II Technical Reference Manual.
        """

        return Esc("f")

    @classmethod
    def reverse(cls: Type[Self]) -> Command:
        """
        Set lines to feed in reverse as per page 71 of the ImageWriter II
        Technical Reference Manual.
        """

        return Esc("r")

    @classmethod
    def set_auto_after_cr(
        cls: Type[Self], settings: SoftwareSwitches, enabled: bool
    ) -> Tuple[SoftwareSwitches, Command]:
        """
        Enable or disable an automatic LF after a CR, as per page 34 of the
        ImageWriter II Technical Reference Manual.
        """

        cmd_cls = CloseSoftwareSwitches if enabled else OpenSoftwareSwitches

        return (
            dataclasses.replace(settings, auto_lf_after_cr=enabled),
            cmd_cls({SoftwareSwitch.AUTO_LF_AFTER_CR}),
        )

    @classmethod
    def set_auto_when_line_full(
        cls: Type[Self], settings: SoftwareSwitches, enabled: bool
    ) -> Tuple[SoftwareSwitches, Command]:
        """
        Configure the automatic insertion of a line feed when the line is full,
        as per page 34 of the ImageWriter II Technical Reference Manual.
        """

        cmd_cls = CloseSoftwareSwitches if enabled else OpenSoftwareSwitches

        return (
            dataclasses.replace(settings, lf_when_line_full=enabled),
            cmd_cls({SoftwareSwitch.LF_WHEN_LINE_FULL}),
        )


def set_perforation_skip(
    settings: SoftwareSwitches, enabled: bool
) -> Tuple[SoftwareSwitches, Command]:
    """
    Configure automatic perforation skip, as per page 34 of the ImageWriter II
    Technical Reference Manual.
    """

    cmd_cls = OpenSoftwareSwitches if enabled else CloseSoftwareSwitches

    return (
        dataclasses.replace(settings, perforation_skip_disabled=not enabled),
        cmd_cls({SoftwareSwitch.PERFORATION_SKIP_DISABLED}),
    )
