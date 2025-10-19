from typing import Self

from imagewriter.encoding.base import Esc
from imagewriter.encoding.switch import (
    fmt_switch_banks,
    fmt_switch_position,
    SetSoftwareSwitches,
)
from imagewriter.switch import SoftwareSwitch


class SetAutoLFAfterCR(SetSoftwareSwitches):
    """
    Enable or disable an automatic LF after a CR, as per page 34 of the
    ImageWriter II Technical Reference Manual.
    """

    def __init__(self: Self, enabled: bool) -> None:
        super().__init__(enabled, {SoftwareSwitch.AUTO_LF_AFTER_CR})

    def __repr__(self: Self) -> str:
        position = fmt_switch_position(self.closed)
        banks = fmt_switch_banks(self.pack())

        return f"SetAutoLFAfterCR({self.closed}, {position}, {banks})"


class SetCarriageReturnInsertion(Esc):
    """
    As per page 75 of the ImageWriter II Technical Reference Manual, when
    carriage return insertion is enabled, a CR (\\r) will be inserted before
    every LF (\\n) or FF (^L) character. This is enabled by default.

    Note that this does not control whether or not LF or FF will
    trigger printing.

    Note that this is also different from automatic LF insertion after a CR,
    the opposite behavior. This is controlled by switches, as per page 77 of
    the ImageWriter II Technical Reference Manual.
    """

    def __init__(self: Self, enabled: bool) -> None:
        self._enabled = enabled
        super().__init__("l1" if enabled else "l0")

    def __repr__(self: Self) -> str:
        return f"SetCarriageReturnInsertion({self._enabled})"


class SetLFWhenLineFull(SetSoftwareSwitches):
    """
    Configure the automatic insertion of a line feed when the line is full,
    as per page 34 of the ImageWriter II Technical Reference Manual.
    """

    def __init__(self: Self, enabled: bool) -> None:
        super().__init__(enabled, {SoftwareSwitch.LF_WHEN_LINE_FULL})

    def __repr__(self: Self) -> str:
        position = fmt_switch_position(self.closed)
        banks = fmt_switch_banks(self.pack())
        return f"SetLFWhenLineFull({self.closed}, {position}, {banks})"
