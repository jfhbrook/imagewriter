from imagewriter.language import Language
from imagewriter.pitch import Pitch
from imagewriter.print import PrintCommands
from imagewriter.quality import Quality
from imagewriter.serial import SerialProtocol
from imagewriter.settings import Settings


def test_default_settings() -> None:
    settings = Settings()

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
