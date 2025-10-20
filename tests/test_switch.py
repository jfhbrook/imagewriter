from imagewriter.language import Language
from imagewriter.pitch import Pitch
from imagewriter.print import PrintCommands
from imagewriter.serial import SerialProtocol
from imagewriter.switch import DIPSwitches, SoftwareSwitches


def test_dip_switch_defaults() -> None:
    switches = DIPSwitches.defaults()

    assert switches.language == Language.AMERICAN
    assert switches.form_length == 11
    assert not switches.perforation_skip
    assert switches.pitch == Pitch.ELITE
    assert not switches.auto_lf_after_cr
    assert switches.baud_rate == 9600
    assert switches.protocol == SerialProtocol.HARDWARE_HANDSHAKE


def test_software_switch_defaults() -> None:
    switches = SoftwareSwitches.defaults()

    assert switches.language == Language.AMERICAN
    assert switches.software_select_response_disabled
    assert not switches.lf_when_line_full
    assert switches.print_commands == PrintCommands.CR_LF_AND_FF
    assert not switches.auto_lf_after_cr
    assert not switches.slashed_zero
    assert switches.perforation_skip_disabled
    assert switches.ignore_eighth_data_bit
