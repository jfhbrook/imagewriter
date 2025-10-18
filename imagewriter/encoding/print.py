import dataclasses
from typing import Tuple

from imagewriter.encoding.base import Command
from imagewriter.encoding.switch import CloseSoftwareSwitches, OpenSoftwareSwitches
from imagewriter.switch import SoftwareSwitch, SoftwareSwitches


def set_print_commands_include_lf_ff(
    settings: SoftwareSwitches, enabled: bool
) -> Tuple[SoftwareSwitches, Command]:
    """
    Configure the treatment of LF and FF as print commands, as per page 34
    of the ImageWriter II Technical Reference Manual.
    """

    cmd_cls = CloseSoftwareSwitches if enabled else OpenSoftwareSwitches

    return (
        dataclasses.replace(settings, print_commands_include_lf_ff=enabled),
        cmd_cls({SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF}),
    )
