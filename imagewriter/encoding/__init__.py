from typing import List

from imagewriter.encoding.attributes import (
    Pitch,
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
from imagewriter.encoding.character import CharacterEncoder, Text
from imagewriter.encoding.distance import Centimeter, Distance, Inch, Millimeter
from imagewriter.encoding.formatting import set_left_margin
from imagewriter.encoding.language import Language
from imagewriter.encoding.switch import SoftwareSwitch

__all__: List[str] = [
    "Pitch",
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
    "CharacterEncoder",
    "Text",
    "Distance",
    "Inch",
    "Centimeter",
    "Millimeter",
    "set_left_margin",
    "Language",
    "SoftwareSwitch",
]
