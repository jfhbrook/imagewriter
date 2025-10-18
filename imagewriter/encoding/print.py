from imagewriter.encoding.base import Command
from imagewriter.encoding.switch import CloseSoftwareSwitches, OpenSoftwareSwitches
from imagewriter.switch import SoftwareSwitch


def set_print_commands_include_lf_ff(enabled: bool) -> Command:
    """
    Configure the treatment of LF and FF as print commands, as per page 34
    of the ImageWriter II Technical Reference Manual.
    """

    cmd_cls = CloseSoftwareSwitches if enabled else OpenSoftwareSwitches

    return cmd_cls({SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF})
