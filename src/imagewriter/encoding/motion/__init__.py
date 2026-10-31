from typing import Self

from imagewriter.base.pitch import Pitch
from imagewriter.base.units import Distance, Length, length_to_int
from imagewriter.encoding.base import (
    Bytes,
    Command,
    Ctrl,
    Esc,
    LengthError,
    esc,
    number,
)
from imagewriter.encoding.motion.form_feed import (
    FF,
    SET_TOP_OF_FORM,
    SetPerforationSkip,
    SetTopOfForm,
)
from imagewriter.encoding.motion.insertion import (
    SetAutoLFAfterCR,
    SetCRInsertion,
    SetLFWhenLineFull,
)
from imagewriter.encoding.motion.line_feed import (
    LF,
    LINE_FEED_FORWARD,
    LINE_FEED_REVERSE,
    LineFeed,
    LineFeedForward,
    LineFeedLengthError,
    LineFeedReverse,
    SetDistanceBetweenLines,
    SetLinesPerInch,
)
from imagewriter.encoding.motion.tab import (
    CLEAR_ALL_TABS,
    TAB,
    ClearAllTabs,
    ClearManyTabs,
    SetManyTabs,
    SetOneTab,
    TabLengthError,
    reset_tabs,
    to_tab_stops,
)


class CarriageReturnLengthError(LengthError):
    """
    An error raised when a carriage return has no meaningful length.
    """


class CarriageReturn(Bytes):
    """
    A carriage return (\\r).
    """

    def __init__(self: Self) -> None:
        super().__init__(b"\r")

    def __repr__(self: Self) -> str:
        return "<CR>"

    def __len__(self: Self) -> int:
        raise CarriageReturnLengthError("\\r does not have a meaningful length")


class BackspaceLengthError(LengthError):
    """
    An error raised when a backspace has an ambiguous length.
    """


class Backspace(Ctrl):
    """
    A backspace.
    """

    def __init__(self: Self) -> None:
        super().__init__("H")

    def __repr__(self: Self) -> str:
        return "Backspace()"

    def __len__(self: Self) -> int:
        raise BackspaceLengthError("Backspace does not have a positive length")


CR = CarriageReturn()
BACKSPACE = Backspace()
CRLF: list[Command] = [CR, LF]


def cr_lf(count: int = 1) -> list[Command]:
    return CRLF * count


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


def _print_head_position(position: Length, pitch: Pitch) -> int:
    def get(position: Distance) -> int:
        return position.horizontal_dpi(pitch)

    return min(length_to_int(position, get), pitch.width)


class PlaceExactPrintHeadPosition(Command):
    """
    Place the exact print head position, as per page 120 of the ImageWriter
    II Technical Reference Manual.

    Position is typically specified in dots per inch, based on the pitch.
    """

    def __init__(self: Self, position: Length, pitch: Pitch) -> None:
        self.position: int = _print_head_position(position, pitch)
        self.pitch: Pitch = pitch

    def __bytes__(self: Self) -> bytes:
        return esc("F") + number(self.position, 4)

    def __repr__(self: Self) -> str:
        return f"PlaceExactPrintHeadPosition({self.position})"


__all__: list[str] = [
    "BACKSPACE",
    "CLEAR_ALL_TABS",
    "CR",
    "CRLF",
    "FF",
    "LF",
    "LINE_FEED_FORWARD",
    "LINE_FEED_REVERSE",
    "SET_TOP_OF_FORM",
    "TAB",
    "Backspace",
    "BackspaceLengthError",
    "CarriageReturn",
    "CarriageReturnLengthError",
    "ClearAllTabs",
    "ClearManyTabs",
    "LineFeed",
    "LineFeedForward",
    "LineFeedLengthError",
    "LineFeedReverse",
    "PlaceExactPrintHeadPosition",
    "SetAutoLFAfterCR",
    "SetCRInsertion",
    "SetDistanceBetweenLines",
    "SetLFWhenLineFull",
    "SetLinesPerInch",
    "SetManyTabs",
    "SetOneTab",
    "SetPerforationSkip",
    "SetTopOfForm",
    "SetUnidirectionalPrinting",
    "TabLengthError",
    "cr_lf",
    "reset_tabs",
    "to_tab_stops",
]
