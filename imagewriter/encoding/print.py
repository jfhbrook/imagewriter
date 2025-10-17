import dataclasses
from typing import Tuple

from imagewriter.encoding.base import Command
from imagewriter.encoding.switch import CloseSoftwareSwitches, OpenSoftwareSwitches
from imagewriter.switch import SoftwareSwitch, SoftwareSwitchSettings


def enable_lf_ff_print_commands(
    settings: SoftwareSwitchSettings,
) -> Tuple[SoftwareSwitchSettings, Command]:
    """
    Enable the treatment of LF and FF as print commands, as per page 34
    of the ImageWriter II Technical Reference Manual.
    """

    return (
        dataclasses.replace(settings, print_commands_include_lf_ff=True),
        CloseSoftwareSwitches({SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF}),
    )


def disable_lf_ff_print_commands(
    settings: SoftwareSwitchSettings,
) -> Tuple[SoftwareSwitchSettings, Command]:
    """
    Disable the treatment of LF and FF as print commands, as per page 34
    of the ImageWriter II Technical Reference Manual.
    """

    return (
        dataclasses.replace(settings, print_commands_include_lf_ff=False),
        OpenSoftwareSwitches({SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF}),
    )
