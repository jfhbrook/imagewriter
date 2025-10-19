from typing import Self

from imagewriter.encoding.switch import (
    fmt_switch_banks,
    fmt_switch_position,
    SetSoftwareSwitches,
)
from imagewriter.switch import SoftwareSwitch


class SetPrintCommandsIncludeLFFF(SetSoftwareSwitches):
    """
    Configure the treatment of LF and FF as print commands, as per page 34
    of the ImageWriter II Technical Reference Manual.
    """

    def __init__(self: Self, enabled: bool) -> None:
        super().__init__(enabled, {SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF})

    def __repr__(self: Self) -> str:
        position = fmt_switch_position(self.closed)
        banks = fmt_switch_banks(self.pack())

        return f"SetPrintCommandsIncludeLFFF({self.closed}, {position}, {banks})"
