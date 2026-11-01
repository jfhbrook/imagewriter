import pytest

from imagewriter.base.character import Language
from imagewriter.base.print import PrintCommands
from imagewriter.base.switch import SoftwareSwitch, SoftwareSwitches
from imagewriter.encoding.attributes import PRINT_SLASHED_ZERO, PRINT_UNSLASHED_ZERO
from imagewriter.encoding.base import esc
from imagewriter.encoding.language import set_language
from imagewriter.encoding.motion import (
    SetAutoLFAfterCR,
    SetLFWhenLineFull,
    SetPerforationSkip,
)
from imagewriter.encoding.print import SetPrintCommands
from imagewriter.encoding.select import SetSoftwareSelectResponse
from imagewriter.encoding.serial import IGNORE_EIGHTH_DATA_BIT, INCLUDE_EIGHTH_DATA_BIT
from imagewriter.encoding.switch import (
    SetSoftwareSwitches,
    apply_software_switches,
)


def test_apply() -> None:
    switches = SoftwareSwitches.from_switches(
        {
            SoftwareSwitch.LANGUAGE_1,
            SoftwareSwitch.SOFTWARE_SELECT_RESPONSE_DISABLED,
            SoftwareSwitch.LF_WHEN_LINE_FULL,
            SoftwareSwitch.PRINT_COMMANDS_INCLUDE_LF_FF,
            SoftwareSwitch.AUTO_LF_AFTER_CR,
            SoftwareSwitch.PERFORATION_SKIP_DISABLED,
            SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT,
        }
    )

    commands = apply_software_switches(switches)

    assert len(commands) == 2, "Should be an open and a close command"

    open_buffer = bytes(commands[0])
    close_buffer = bytes(commands[1])

    assert len(open_buffer) == 4, "First command should have 3 bytes"
    assert open_buffer[0:2] == esc("Z"), "First command should open switches"
    assert bin(open_buffer[2]) == "0b110", "Bank A should open switches"
    assert bin(open_buffer[3]) == "0b1", "Bank B should open switches"

    assert len(close_buffer) == 4, "Second command should have 3 bytes"
    assert close_buffer[0:2] == esc("D"), "Second command should open switches"
    assert bin(close_buffer[2]) == "0b11110001", "Bank A should close switches"
    assert bin(close_buffer[3]) == "0b100100", "Bank B should close switches"


SET_LANGUAGE_AMERICAN = set_language(Language.AMERICAN)
SET_LANGUAGE_SPANISH = set_language(Language.SPANISH)
SET_LANGUAGE_DANISH = set_language(Language.DANISH)


@pytest.mark.parametrize(
    "command,repr_",
    [
        (PRINT_SLASHED_ZERO, "PrintSlashedZero(CLOSE, [0b00000000, 0b00000001])"),
        (PRINT_UNSLASHED_ZERO, "PrintUnslashedZero(OPEN, [0b00000000, 0b00000001])"),
        (
            SetAutoLFAfterCR(True),
            "SetAutoLFAfterCR(True, CLOSE, [0b10000000, 0b00000000])",
        ),
        (
            SetAutoLFAfterCR(False),
            "SetAutoLFAfterCR(False, OPEN, [0b10000000, 0b00000000])",
        ),
        (
            SetLFWhenLineFull(True),
            "SetLFWhenLineFull(True, CLOSE, [0b00100000, 0b00000000])",
        ),
        (
            SetLFWhenLineFull(False),
            "SetLFWhenLineFull(False, OPEN, [0b00100000, 0b00000000])",
        ),
        (
            SetPerforationSkip(True),
            "SetPerforationSkip(True, OPEN, [0b00000000, 0b00000100])",
        ),
        (
            SetPerforationSkip(False),
            "SetPerforationSkip(False, CLOSE, [0b00000000, 0b00000100])",
        ),
        (
            SetPrintCommands(PrintCommands.CR_LF_AND_FF),
            (
                "SetPrintCommands(PrintCommands.CR_LF_AND_FF, "
                "CLOSE, [0b01000000, 0b00000000])"
            ),
        ),
        (
            SetPrintCommands(PrintCommands.CR_ONLY),
            "SetPrintCommands(PrintCommands.CR_ONLY, OPEN, [0b01000000, 0b00000000])",
        ),
        (
            SetSoftwareSelectResponse(True),
            "SetSoftwareSelectResponse(True, OPEN, [0b00010000, 0b00000000])",
        ),
        (
            SetSoftwareSelectResponse(False),
            "SetSoftwareSelectResponse(False, CLOSE, [0b00010000, 0b00000000])",
        ),
        (
            IGNORE_EIGHTH_DATA_BIT,
            "SetIncludeEighthDataBit(False, CLOSE, [0b00000000, 0b00100000])",
        ),
        (
            INCLUDE_EIGHTH_DATA_BIT,
            "SetIncludeEighthDataBit(True, OPEN, [0b00000000, 0b00100000])",
        ),
        (
            SET_LANGUAGE_AMERICAN[0],
            "OpenLanguageSwitches(Language.AMERICAN, OPEN, [0b00000111, 0b00000000])",
        ),
        (
            SET_LANGUAGE_SPANISH[0],
            "CloseLanguageSwitches(Language.SPANISH, CLOSE, [0b00000111, 0b00000000])",
        ),
        (
            SET_LANGUAGE_DANISH[0],
            "OpenLanguageSwitches(Language.DANISH, OPEN, [0b00000101, 0b00000000])",
        ),
        (
            SET_LANGUAGE_DANISH[1],
            "CloseLanguageSwitches(Language.DANISH, CLOSE, [0b00000010, 0b00000000])",
        ),
    ],
)
def test_command(command: SetSoftwareSwitches, repr_: str) -> None:
    packed: bytes = command.pack()
    assert len(packed) == 2

    assert repr(command) == repr_
