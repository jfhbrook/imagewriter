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

import dataclasses
from typing import Tuple

from imagewriter.encoding.base import Command, Ctrl
from imagewriter.encoding.switch import CloseSoftwareSwitches, OpenSoftwareSwitches
from imagewriter.switch import SoftwareSwitch, SoftwareSwitches

SELECT = Ctrl("Q")
DESELECT = Ctrl("S")


def set_software_select_response(
    settings: SoftwareSwitches, enabled: bool
) -> Tuple[SoftwareSwitches, Command]:
    """
    Configure Software Select-Deselect Response, as per page 34 of the
    ImageWriter II Technical Reference Manual.
    """

    cmd_cls = OpenSoftwareSwitches if enabled else CloseSoftwareSwitches

    return (
        dataclasses.replace(settings, software_select_response_disabled=not enabled),
        cmd_cls({SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED}),
    )
