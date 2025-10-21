from typing import List

from imagewriter.encoding.base import Command
from imagewriter.encoding.boundaries import SetLeftMargin, SetPageLength
from imagewriter.encoding.motion import (
    reset_tabs,
    SetCarriageReturnInsertion,
    SetDistanceBetweenLines,
    to_tab_stops,
)
from imagewriter.encoding.paper import SetPaperOutSensor
from imagewriter.encoding.pitch import SetPitch
from imagewriter.encoding.quality import SetQuality
from imagewriter.encoding.switch import apply_software_switches
from imagewriter.settings import Settings


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
        *reset_tabs(to_tab_stops(settings.tab_stops, settings.pitch)),
    ]
