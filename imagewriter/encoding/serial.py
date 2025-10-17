from imagewriter.encoding.base import Command
from imagewriter.encoding.switch import CloseSoftwareSwitches, OpenSoftwareSwitches
from imagewriter.switch import SoftwareSwitch


def ignore_eighth_data_bit() -> Command:
    """
    Ignore the eighth data bit of each byte sent, as per page 34 of the
    ImageWriter II Technical Reference Manual.

    This setting is for the benefit of Applesoft Basic, which does not
    support an eighth bit. Pure ASCII does not use the eighth bit, and the
    ImageWriter II supports escape sequences for "high-ASCII", as per
    Chapter 4 and Chapter 7 of the manual.

    Note that the ImageWriter II will automatically switch to 8-bit mode
    when an escape sequence sent to it uses 8-bit data - examples include
    custom characters and graphics.
    """

    return CloseSoftwareSwitches({SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT})


def include_eighth_data_bit() -> Command:
    """
    Include the eighth data bit of each byte sent, as per page 34 of the
    ImageWriter II Technical Reference Manual.

    This setting is for the benefit of Applesoft Basic, which does not
    support an eighth bit. Pure ASCII does not use the eighth bit, and the
    ImageWriter II supports escape sequences for "high-ASCII", as per
    Chapter 4 and Chapter 7 of the manual.

    Note that the ImageWriter II will automatically switch to 8-bit mode
    when an escape sequence sent to it uses 8-bit data - examples include
    custom characters and graphics.
    """

    return OpenSoftwareSwitches({SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT})
