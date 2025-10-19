from typing import Self

from imagewriter.encoding.switch import (
    fmt_switch_banks,
    fmt_switch_position,
    SetSoftwareSwitches,
)
from imagewriter.switch import SoftwareSwitch


class SetIncludeEighthDataBit(SetSoftwareSwitches):
    """
    Ignore or include the eighth data bit of each byte sent, as per page 34 of
    the ImageWriter II Technical Reference Manual.

    This setting is for the benefit of Applesoft Basic, which does not
    support an eighth bit. Pure ASCII does not use the eighth bit, and the
    ImageWriter II supports escape sequences for "high-ASCII", as per
    Chapter 4 and Chapter 7 of the manual.

    Note that the ImageWriter II will automatically switch to 8-bit mode
    when an escape sequence sent to it uses 8-bit data - examples include
    custom characters and graphics.
    """

    def __init__(self: Self, included: bool) -> None:
        super().__init__(not included, {SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT})

    def __repr__(self: Self) -> str:
        position = fmt_switch_position(self.closed)
        banks = fmt_switch_banks(self.pack())

        return f"SetIncludeEighthDataBit({not self.closed}, {position}, {banks})"


IGNORE_EIGHTH_DATA_BIT = SetIncludeEighthDataBit(False)
INCLUDE_EIGHTH_DATA_BIT = SetIncludeEighthDataBit(True)
