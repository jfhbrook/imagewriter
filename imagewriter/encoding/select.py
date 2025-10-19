"""
Select and deselect commands are equivalent to toggling the SELECT button on
the front panel of the ImageWriter II. As per page 42 of the ImageWriter II
Owner's Manual, the printer will stop responding to commands other than
deselect.

Note that, when selected, the ImageWriter II will set its DTR signal to false,
meaning any device using software select will need to ignore its DTR signal
(typically wired to the CTS line under rs-232) in order to deselect the
printer.

By default, the ImageWriter II will not respond to these commands. To enable
them, open the "software select response" software switch.

See page 87 of the ImageWriter II Technical Reference Manual for more details.
"""

from typing import Self

from imagewriter.encoding.base import Ctrl
from imagewriter.encoding.switch import SetSoftwareSwitches
from imagewriter.switch import SoftwareSwitch


class Select(Ctrl):
    """
    Select the ImageWriter II.
    """

    def __init__(self: Self) -> None:
        super().__init__("Q")

    def __repr__(self: Self) -> str:
        return "Select()"


class Deselect(Ctrl):
    """
    Deselect the ImageWriter II.
    """

    def __init__(self: Self) -> None:
        super().__init__("S")

    def __repr__(self: Self) -> str:
        return "Deselect()"


SELECT = Select()
DESELECT = Deselect()


class SetSoftwareSelectResponse(SetSoftwareSwitches):
    """
    Configure Software Select-Deselect Response, as per page 34 of the
    ImageWriter II Technical Reference Manual.
    """

    def __init__(self: Self, enabled: bool) -> None:
        self._enabled = enabled
        super().__init__(
            not enabled, {SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED}
        )

    def __repr__(self: Self) -> str:
        packed = self.pack()
        return (
            f"SetSoftwareSelectResponse({self._enabled}, {packed[0]:b} {packed[1]:b})"
        )
