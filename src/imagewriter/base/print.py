"""
Print commands, as per page 34 of the ImageWriter II Technical
Reference Manual.

Print commands are character sequences that cause the ImageWriter II to print what's in
its buffer. Typically, a CR will trigger printing. But the ImageWriter II can also be
configured to require both a CR and a LF.
"""

from enum import Enum


class PrintCommands(Enum):
    """
    Settings for valid print commands.
    """

    CR_ONLY = False
    CR_LF_AND_FF = True
