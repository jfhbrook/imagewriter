import dataclasses

from imagewriter.encoding.base import esc
from imagewriter.encoding.switch import update_software_switch_settings
from imagewriter.switch import SoftwareSwitch, SoftwareSwitches


def test_toggle() -> None:
    switches = {
        SoftwareSwitch.LANGUAGE_1,
        SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED,
        SoftwareSwitch.LF_WHEN_LINE_FULL,
        SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF,
        SoftwareSwitch.AUTO_LF_AFTER_CR,
        SoftwareSwitch.PERFORATION_SKIP_DISABLED,
        SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT,
    }

    before = SoftwareSwitches.from_switches(SoftwareSwitch.difference(switches))
    after = SoftwareSwitches.from_switches(switches)

    print(before)
    print(after)

    _, commands = update_software_switch_settings(before, **dataclasses.asdict(after))

    assert len(commands) == 2, "Should be an open and a close command"

    open_buffer = bytes(commands[0])
    close_buffer = bytes(commands[1])

    assert len(open_buffer) == 4, "First command should have 3 bytes"
    assert open_buffer[0:2] == esc("Z"), "First command should open switches"
    assert bin(open_buffer[2]) == "0b1100000", "Bank A should open switches"
    assert bin(open_buffer[3]) == "0b10000000", "Bank B should open switches"

    assert len(close_buffer) == 4, "Second command should have 3 bytes"
    assert close_buffer[0:2] == esc("D"), "Second command should open switches"
    assert bin(close_buffer[2]) == "0b10001111", "Bank A should close switches"
    assert bin(close_buffer[3]) == "0b100100", "Bank B should close switches"
