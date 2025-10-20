from imagewriter.language import Language
from imagewriter.pitch import Pitch
from imagewriter.print import PrintCommands
from imagewriter.quality import Quality
from imagewriter.serial import SerialProtocol
from imagewriter.settings import Settings
from imagewriter.switch import DIPSwitches, SoftwareSwitches


def test_default_settings() -> None:
    dip_switches = DIPSwitches.defaults()
    software_switches = SoftwareSwitches.defaults(dip_switches)
    settings = Settings()

    # dip switches
    assert settings.language == dip_switches.language
    assert settings.page_length.inches == dip_switches.form_length
    assert settings.perforation_skip == dip_switches.perforation_skip
    assert settings.pitch == dip_switches.pitch
    assert settings.baud_rate == dip_switches.baud_rate
    assert settings.protocol == dip_switches.protocol

    # software switches
    assert settings.language == software_switches.language
    assert (
        settings.software_select_response
        != software_switches.software_select_response_disabled
    )
    assert settings.lf_when_line_full == software_switches.lf_when_line_full
    assert settings.print_commands == software_switches.print_commands
    assert settings.auto_lf_after_cr == software_switches.auto_lf_after_cr
    assert settings.slashed_zero is software_switches.slashed_zero
    assert settings.perforation_skip != software_switches.perforation_skip_disabled
    assert settings.include_eighth_data_bit != software_switches.ignore_eighth_data_bit

    # boundaries
    assert settings.left_margin.inches == 0
    assert settings.page_length.inches == 11
    # fonts and pitch
    assert settings.language == Language.AMERICAN
    assert not settings.slashed_zero
    assert settings.pitch == Pitch.ELITE
    # motion and insertion
    assert len(settings.tab_stops) == 0
    assert settings.distance_between_lines.picas == 1
    assert not settings.lf_when_line_full
    assert not settings.auto_lf_after_cr
    assert not settings.carriage_return_insertion
    assert not settings.perforation_skip
    # paper
    assert settings.paper_out_sensor
    # print commands
    assert settings.print_commands == PrintCommands.CR_LF_AND_FF
    # quality
    assert settings.quality == Quality.DRAFT
    # select
    assert not settings.software_select_response
    # serial
    assert settings.baud_rate == 9600
    assert settings.protocol == SerialProtocol.HARDWARE_HANDSHAKE
    assert not settings.include_eighth_data_bit
