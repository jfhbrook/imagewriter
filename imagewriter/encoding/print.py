from imagewriter.encoding.base import Command
from imagewriter.encoding.switch import CloseSoftwareSwitches, OpenSoftwareSwitches
from imagewriter.switch import SoftwareSwitch


def enable_lf_ff_print_commands() -> Command:
    """
    Enable the treatment of LF and FF as print commands, as per page 34
    of the ImageWriter II Technical Reference Manual.
    """

    return CloseSoftwareSwitches({SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF})


def disable_lf_ff_print_commands() -> Command:
    """
    Disable the treatment of LF and FF as print commands, as per page 34
    of the ImageWriter II Technical Reference Manual.
    """

    return OpenSoftwareSwitches({SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF})
