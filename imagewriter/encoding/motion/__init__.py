from typing import List, Self

from imagewriter.encoding.base import (
    Bytes,
    Command,
    Ctrl,
    esc,
    Esc,
    LengthError,
    number,
)
from imagewriter.encoding.motion.form_feed import (
    FF,
    SET_TOP_OF_FORM,
    SetPerforationSkip,
)
from imagewriter.encoding.motion.insertion import (
    SetAutoLFAfterCR,
    SetCRInsertion,
    SetLFWhenLineFull,
)
from imagewriter.encoding.motion.line_feed import (
    LF,
    LineFeed,
    LineFeedForward,
    LineFeedLengthError,
    LineFeedReverse,
    SetDistanceBetweenLines,
    SetLinesPerInch,
)
from imagewriter.encoding.motion.tab import (
    ClearAllTabs,
    ClearManyTabs,
    reset_tabs,
    SetManyTabs,
    SetOneTab,
    TAB,
    TabLengthError,
    to_tab_stops,
)
from imagewriter.pitch import Pitch
from imagewriter.units import Distance, Length, length_to_int


class CarriageReturnLengthError(LengthError):
    """
    An error raised when a carriage return has no meaningful length.
    """

    pass


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


__all__: List[str] = [
    "CarriageReturn",
    "CarriageReturnLengthError",
    "CR",
    "Backspace",
    "BACKSPACE",
    "BackspaceLengthError",
    "SetUnidirectionalPrinting",
    "PlaceExactPrintHeadPosition",
    "FF",
    "SET_TOP_OF_FORM",
    "SetPerforationSkip",
    "SetAutoLFAfterCR",
    "SetCRInsertion",
    "SetLFWhenLineFull",
    "LF",
    "LineFeed",
    "LineFeedForward",
    "LineFeedLengthError",
    "LineFeedReverse",
    "SetDistanceBetweenLines",
    "SetLinesPerInch",
    "ClearAllTabs",
    "ClearManyTabs",
    "reset_tabs",
    "SetManyTabs",
    "SetOneTab",
    "TAB",
    "TabLengthError",
    "to_tab_stops",
]
