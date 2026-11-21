from parsy import Parser, alt  # type: ignore

from imagewriter.base.print import PrintCommands
from imagewriter.base.switch import SoftwareSwitch
from imagewriter.decoding.base import State
from imagewriter.decoding.switch import close_software_switch, open_software_switch
from imagewriter.encoding.print import SetPrintCommands


def set_print_commands(state: State) -> Parser:
    return alt(
        close_software_switch(
            state,
            SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF,
            SetPrintCommands(PrintCommands.CR_LF_AND_FF),
        ),
        open_software_switch(
            state,
            SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF,
            SetPrintCommands(PrintCommands.CR_ONLY),
        ),
    )
