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
from imagewriter.encoding.base import ctrl, esc
from imagewriter.encoding.boundaries import set_left_margin, set_page_length
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
    print_graphics_data,
    set_graphics_distance_between_lines,
)
from imagewriter.encoding.insertion import (
    DISABLE_CARRIAGE_RETURN_INSERTION,
    ENABLE_CARRIAGE_RETURN_INSERTION,
)
from imagewriter.encoding.language import Language
from imagewriter.encoding.motion import (
    BACKSPACE,
    CR,
    LF,
    LineFeed,
    place_exact_print_head_position,
    SET_TOP_OF_FORM,
    set_unidirectional_printing,
    TAB,
    TabStops,
)
from imagewriter.encoding.paper import DISABLE_PAPER_OUT_SENSOR, ENABLE_PAPER_OUT_SENSOR
from imagewriter.encoding.pitch import Pitch
from imagewriter.encoding.quality import Quality
from imagewriter.encoding.repeat import repeat
from imagewriter.encoding.reset import RESET
from imagewriter.encoding.select import DESELECT, SELECT
from imagewriter.encoding.switch import SoftwareSwitch
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
    "ctrl",
    "esc",
    "set_left_margin",
    "set_page_length",
    "CANCEL_CURRENT_LINE",
    "CharacterEncoder",
    "Text",
    "BOTTOM_WIRES",
    "character_data",
    "CustomCharacter",
    "TOP_WIRES",
    "Color",
    "print_graphics_data",
    "set_graphics_distance_between_lines",
    "DISABLE_CARRIAGE_RETURN_INSERTION",
    "ENABLE_CARRIAGE_RETURN_INSERTION",
    "Language",
    "BACKSPACE",
    "CR",
    "LF",
    "LineFeed",
    "place_exact_print_head_position",
    "SET_TOP_OF_FORM",
    "set_unidirectional_printing",
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
