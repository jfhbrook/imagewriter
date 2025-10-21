from typing import List

from imagewriter.encoding.base import Command
from imagewriter.encoding.boundaries import SetLeftMargin, SetPageLength
from imagewriter.encoding.motion import (
    reset_tabs,
    SetCarriageReturnInsertion,
    SetDistanceBetweenLines,
)
from imagewriter.encoding.paper import SetPaperOutSensor
from imagewriter.encoding.pitch import SetPitch
from imagewriter.encoding.quality import SetQuality
from imagewriter.encoding.switch import apply_software_switches
from imagewriter.settings import Settings
from imagewriter.units import length_to_int


def apply_settings(settings: Settings) -> List[Command]:
    return [
        *apply_software_switches(settings.switches()),
        SetCarriageReturnInsertion(settings.carriage_return_insertion),
        SetPaperOutSensor(settings.paper_out_sensor),
        SetPitch(settings.pitch),
        SetQuality(settings.quality),
        SetLeftMargin(settings.left_margin, settings.pitch),
        SetPageLength(settings.page_length),
        SetDistanceBetweenLines(settings.distance_between_lines),
        *reset_tabs(
            [
                length_to_int(stop, lambda st: st.characters(settings.pitch))
                for stop in settings.tab_stops
            ]
        ),
    ]
