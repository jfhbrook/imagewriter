from parsy import Parser, alt  # type: ignore

from imagewriter.base.switch import SoftwareSwitch
from imagewriter.decoding.base import State
from imagewriter.decoding.switch import close_software_switch, open_software_switch
from imagewriter.encoding.serial import IGNORE_EIGHTH_DATA_BIT, INCLUDE_EIGHTH_DATA_BIT


def set_include_eighth_data_bit(state: State) -> Parser:
    return alt(
        close_software_switch(
            state, SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT, IGNORE_EIGHTH_DATA_BIT
        ),
        open_software_switch(
            state, SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT, INCLUDE_EIGHTH_DATA_BIT
        ),
    )
