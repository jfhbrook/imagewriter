from typing import List

from imagewriter.encoding import (
    boldface,
    CharacterEncoder,
    Command,
    CR,
    double_width,
    half_height,
    PRINT_SLASHED_ZERO,
    PRINT_UNSLASHED_ZERO,
    START_SUBSCRIPT,
    START_SUPERSCRIPT,
    STOP_SUBSCRIPT,
    underline,
)

encoder: CharacterEncoder = CharacterEncoder()

ATTRIBUTES_TEST: List[Command] = [
    *encoder.encode("Plain\r\n"),
    *double_width(encoder.encode("Double width\r\n")),
    *underline(encoder.encode("Underlined\r\n")),
    *boldface(encoder.encode("Boldface\r\n")),
    *half_height(encoder.encode("Half height\r\n")),
    START_SUPERSCRIPT,
    *encoder.encode("Superscript\r\n"),
    START_SUBSCRIPT,
    *encoder.encode("Subscript\r\n"),
    STOP_SUBSCRIPT,
    PRINT_UNSLASHED_ZERO,
    *encoder.encode("Unslashed 0\r\n"),
    PRINT_SLASHED_ZERO,
    *encoder.encode("Slashed 0\r\n"),
    CR,
]
