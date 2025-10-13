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
from imagewriter.encoding.character import CharacterEncoder, Text
from imagewriter.encoding.language import Language
from imagewriter.encoding.length import Centimeter, Inch, Length, Millimeter
from imagewriter.encoding.motion import (
    BACKSPACE,
    CR,
    LF,
    place_exact_print_head_position,
    SET_TOP_OF_FORM,
    set_unidirectional_printing,
    TAB,
    TabStops,
)
from imagewriter.encoding.pitch import Pitch
from imagewriter.encoding.quality import Quality
from imagewriter.encoding.switch import SoftwareSwitch

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
    "CharacterEncoder",
    "Text",
    "Language",
    "Inch",
    "Centimeter",
    "Length",
    "Millimeter",
    "BACKSPACE",
    "CR",
    "LF",
    "place_exact_print_head_position",
    "SET_TOP_OF_FORM",
    "set_unidirectional_printing",
    "TAB",
    "TabStops",
    "Pitch",
    "Quality",
    "SoftwareSwitch",
]
