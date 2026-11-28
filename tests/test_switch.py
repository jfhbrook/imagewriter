import pytest

from imagewriter.base.character import Language
from imagewriter.base.pitch import Pitch
from imagewriter.base.print import PrintCommands
from imagewriter.base.switch import (
    DIPSwitches,
    SoftwareSwitch,
    SoftwareSwitches,
    SoftwareSwitchLanguage,
)
from imagewriter.serial import SerialProtocol


def test_dip_switch_defaults(dip_switches: DIPSwitches) -> None:
    assert dip_switches.language == Language.AMERICAN
    assert dip_switches.form_length == 11
    assert not dip_switches.perforation_skip
    assert dip_switches.pitch == Pitch.ELITE
    assert not dip_switches.auto_lf_after_cr
    assert dip_switches.baud_rate == 9600
    assert dip_switches.protocol == SerialProtocol.HARDWARE_HANDSHAKE


def test_software_switch_defaults(software_switches: SoftwareSwitches) -> None:
    assert software_switches.language == Language.AMERICAN
    assert software_switches.software_select_response_disabled
    assert not software_switches.lf_when_line_full
    assert software_switches.print_commands == PrintCommands.CR_LF_AND_FF
    assert not software_switches.auto_lf_after_cr
    assert not software_switches.slashed_zero
    assert software_switches.perforation_skip_disabled
    assert software_switches.ignore_eighth_data_bit


@pytest.mark.parametrize(
    "language,switches",
    [
        (Language.AMERICAN, set()),
        (Language.BRITISH, {SoftwareSwitch.LANGUAGE_1, SoftwareSwitch.LANGUAGE_2}),
        (Language.GERMAN, {SoftwareSwitch.LANGUAGE_3}),
        (Language.FRENCH, {SoftwareSwitch.LANGUAGE_2, SoftwareSwitch.LANGUAGE_3}),
        (Language.SWEDISH, {SoftwareSwitch.LANGUAGE_1, SoftwareSwitch.LANGUAGE_3}),
        (Language.ITALIAN, {SoftwareSwitch.LANGUAGE_1}),
        (
            Language.SPANISH,
            {
                SoftwareSwitch.LANGUAGE_1,
                SoftwareSwitch.LANGUAGE_2,
                SoftwareSwitch.LANGUAGE_3,
            },
        ),
        (Language.DANISH, {SoftwareSwitch.LANGUAGE_2}),
    ],
)
def test_software_switch_language(
    language: Language, switches: set[SoftwareSwitch]
) -> None:
    assert SoftwareSwitchLanguage.closed(language) == switches
