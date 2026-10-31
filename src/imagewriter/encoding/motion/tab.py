from collections.abc import Sequence
from typing import Self

from imagewriter.base.pitch import Pitch
from imagewriter.base.units import Length, length_to_int
from imagewriter.encoding.base import Bytes, Command, Esc, LengthError, esc, number


class TabLengthError(LengthError):
    """
    An error raised when a tab character does not have a known length.
    """


class Tab(Bytes):
    """
    A tab character (\\t).
    """

    def __init__(self: Self) -> None:
        super().__init__(b"\t")

    def __repr__(self: Self) -> str:
        return "<TAB>"

    def __len__(self: Self) -> int:
        raise TabLengthError("Tab's length depends on tab stops and pitch")


TAB = Tab()


def to_tab_stops(stops: Sequence[Length], pitch: Pitch) -> list[int]:
    return [length_to_int(stop, lambda st: st.characters(pitch)) for stop in stops]


def _encode_tab_stops(stops: list[int]) -> bytes:
    tab_stops: list[int] = sorted(stops)

    encoded: bytes = b""

    for stop in tab_stops:
        encoded += number(stop, 3)

    encoded = encoded[:-1] + b"."

    return encoded


class SetManyTabs(Bytes):
    """
    Set multiple tab stops, as per page 65 of the ImageWriter II Technical
    Reference Manual.
    """

    def __init__(self: Self, stops: list[int]) -> None:
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

    def __init__(self: Self, stops: list[int]) -> None:
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


CLEAR_ALL_TABS = ClearAllTabs()


def reset_tabs(stops: list[int]) -> list[Command]:
    """
    Clear and then set stops, effectively resetting them.

    As per page 68 of the ImageWriter II Technical Reference Manual, if
    the pitch is changed, the tab stops remain in their existing locations
    and no longer correspond to character column positions. Therefore,
    when changing the pitch, it is recommended to reset tab positions.
    """

    clear_all: Command = ClearAllTabs()
    set_many: Command = SetManyTabs(stops)

    commands: list[Command] = [clear_all]

    if stops:
        commands.append(set_many)

    return commands
