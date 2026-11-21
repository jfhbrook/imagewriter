from parsy import Parser, alt  # type: ignore

from imagewriter.base.switch import SoftwareSwitch
from imagewriter.decoding.base import State, ctrl_command
from imagewriter.decoding.switch import close_software_switch, open_software_switch
from imagewriter.encoding.select import DESELECT, SELECT, SetSoftwareSelectResponse

select = ctrl_command(SELECT)
deselect = ctrl_command(DESELECT)


def set_software_select_response(state: State) -> Parser:
    return alt(
        close_software_switch(
            state,
            SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED,
            SetSoftwareSelectResponse(False),
        ),
        open_software_switch(
            state,
            SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED,
            SetSoftwareSelectResponse(True),
        ),
    )
