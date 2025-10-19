from enum import Enum


class PrintCommands(Enum):
    """
    Settings for valid print commands.
    """

    CR_ONLY = False
    CR_LF_AND_FF = True
