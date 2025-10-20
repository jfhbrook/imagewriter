from typing import List, Self

from imagewriter.encoding.base import (
    Bytes,
    Command,
    esc,
    Esc,
    number,
)


class Tab(Bytes):
    """
    A tab character (\\t).
    """

    def __init__(self: Self) -> None:
        super().__init__(b"\t")

    def __repr__(self: Self) -> str:
        return "\\t"


TAB = Tab()


def _encode_tab_stops(stops: List[int]) -> bytes:
    tab_stops: List[int] = sorted(stops)

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

    commands: List[Command] = [clear_all]

    if stops:
        commands.append(set_many)

    return commands
