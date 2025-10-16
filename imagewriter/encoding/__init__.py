from typing import List

from imagewriter.encoding.attributes import (
    START_BOLDFACE,
    START_DOUBLE_WIDTH,
    START_HALF_HEIGHT,
    START_SUBSCRIPT,
    START_SUPERSCRIPT,
    START_UNDERLINE,
    STOP_BOLDFACE,
    STOP_DOUBLE_WIDTH,
    STOP_HALF_HEIGHT,
    STOP_SUBSCRIPT,
    STOP_SUPERSCRIPT,
    STOP_UNDERLINE,
)
from imagewriter.encoding.base import Bytes, Command, ctrl, Ctrl, esc, Esc, NULL
from imagewriter.encoding.boundaries import SetLeftMargin, SetPageLength
from imagewriter.encoding.cancel import CANCEL_CURRENT_LINE
from imagewriter.encoding.character import CharacterEncoder, Text
from imagewriter.encoding.character.custom import (
    BOTTOM_WIRES,
    character_data,
    CustomCharacter,
    TOP_WIRES,
)
from imagewriter.encoding.color import Color
from imagewriter.encoding.graphics import (
    PrintGraphicsData,
    set_graphics_distance_between_lines,
)
from imagewriter.encoding.insertion import (
    DISABLE_CARRIAGE_RETURN_INSERTION,
    ENABLE_CARRIAGE_RETURN_INSERTION,
)
from imagewriter.encoding.motion import (
    BACKSPACE,
    CR,
    LF,
    LineFeed,
    PlaceExactPrintHeadPosition,
    SET_TOP_OF_FORM,
    SetUnidirectionalPrinting,
    TAB,
    TabStops,
)
from imagewriter.encoding.paper import DISABLE_PAPER_OUT_SENSOR, ENABLE_PAPER_OUT_SENSOR
from imagewriter.encoding.pitch import Pitch
from imagewriter.encoding.quality import Quality
from imagewriter.encoding.repeat import repeat
from imagewriter.encoding.reset import RESET
from imagewriter.encoding.select import DESELECT, SELECT
from imagewriter.encoding.switch import (
    CloseSoftwareSwitches,
    OpenSoftwareSwitches,
    SoftwareSwitch,
)
from imagewriter.encoding.units import (
    Centimeter,
    Distance,
    Inch,
    Length,
    length_to_distance,
    length_to_int,
    Millimeter,
    Pica,
    Point,
)

__all__: List[str] = [
    "START_DOUBLE_WIDTH",
    "STOP_DOUBLE_WIDTH",
    "START_UNDERLINE",
    "STOP_UNDERLINE",
    "START_BOLDFACE",
    "STOP_BOLDFACE",
    "START_HALF_HEIGHT",
    "STOP_HALF_HEIGHT",
    "START_SUPERSCRIPT",
    "STOP_SUPERSCRIPT",
    "START_SUBSCRIPT",
    "STOP_SUBSCRIPT",
    "Bytes",
    "ctrl",
    "Ctrl",
    "esc",
    "Esc",
    "NULL",
    "Command",
    "SetLeftMargin",
    "SetPageLength",
    "CANCEL_CURRENT_LINE",
    "CharacterEncoder",
    "Text",
    "BOTTOM_WIRES",
    "character_data",
    "CustomCharacter",
    "TOP_WIRES",
    "Color",
    "PrintGraphicsData",
    "set_graphics_distance_between_lines",
    "DISABLE_CARRIAGE_RETURN_INSERTION",
    "ENABLE_CARRIAGE_RETURN_INSERTION",
    "BACKSPACE",
    "CR",
    "LF",
    "LineFeed",
    "PlaceExactPrintHeadPosition",
    "SET_TOP_OF_FORM",
    "SetUnidirectionalPrinting",
    "TAB",
    "TabStops",
    "DISABLE_PAPER_OUT_SENSOR",
    "ENABLE_PAPER_OUT_SENSOR",
    "Pitch",
    "Quality",
    "repeat",
    "RESET",
    "DESELECT",
    "SELECT",
    "CloseSoftwareSwitches",
    "OpenSoftwareSwitches",
    "SoftwareSwitch",
    "Centimeter",
    "Distance",
    "Inch",
    "Length",
    "length_to_distance",
    "length_to_int",
    "Millimeter",
    "Pica",
    "Point",
]
