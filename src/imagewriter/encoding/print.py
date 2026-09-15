from typing import Self

from imagewriter.encoding.switch import (
    fmt_switch_banks,
    fmt_switch_position,
    SetSoftwareSwitches,
)
from imagewriter.print import PrintCommands
from imagewriter.switch import SoftwareSwitch


class SetPrintCommands(SetSoftwareSwitches):
    """
    Configure print commands, as per page 34 of the ImageWriter II Technical
    Reference Manual.
    """

    def __init__(self: Self, print_commands: PrintCommands) -> None:
        self._print_commands = print_commands
        super().__init__(
            print_commands.value, {SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF}
        )

    def __repr__(self: Self) -> str:
        position = fmt_switch_position(self.closed)
        banks = fmt_switch_banks(self.pack())

        return f"SetPrintCommands({self._print_commands}, {position}, {banks})"
