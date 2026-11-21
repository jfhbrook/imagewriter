from collections.abc import Callable, Generator
from typing import Any

from parsy import Parser, alt, any_char, generate  # type: ignore

from imagewriter.base.character.custom import (
    CustomCharacter,
    CustomCharacterData,
    Wires,
)
from imagewriter.decoding.base import bytes_, ctrl, esc, esc_command
from imagewriter.encoding.character.base import DISABLE_MODE
from imagewriter.encoding.character.custom import (
    CUSTOM_CHARACTER_WIDTH_CODES,
    EnableCustomCharacterMode,
    LoadCustomCharacters,
    SetMaxCustomCharacterWidth,
)
from imagewriter.encoding.character.mousetext import ENABLE_MOUSETEXT_MAPPING_MODE

disable_mode = esc_command(DISABLE_MODE)
enable_mousetext_mapping_mode = esc_command(ENABLE_MOUSETEXT_MAPPING_MODE)
set_max_custom_character_width = alt(
    esc_command(SetMaxCustomCharacterWidth(8)),
    esc_command(SetMaxCustomCharacterWidth(16)),
)


_start_custom_character_load = esc("I")
_stop_custom_character_load = ctrl("D")


def _map_character_width(
    width: int, wires: Wires
) -> Callable[[bytes], tuple[int, Wires]]:
    return lambda _: (width, wires)


_character_width = alt(
    *[
        bytes_(code).map(_map_character_width(width, wires))
        for wires, lookup in CUSTOM_CHARACTER_WIDTH_CODES.items()
        for width, code in lookup.items()
    ]
)

_character_point = any_char.map(lambda b: b[0])


def _character_bytes(width: int) -> Parser:
    return any_char.times(width).concat()


@generate
def _character_data() -> Generator[Parser, Any, CustomCharacterData]:
    point: int = yield _character_point
    width, wires = yield _character_width
    data: bytes = yield _character_bytes(width)

    return CustomCharacterData(character=CustomCharacter(point), data=data, wires=wires)


@generate
def load_custom_character_data() -> Generator[
    Parser, list[CustomCharacterData], LoadCustomCharacters
]:

    yield _start_custom_character_load

    characters = yield _character_data.until(_stop_custom_character_load)

    yield _stop_custom_character_load

    return LoadCustomCharacters(characters)


enable_custom_character_mode = alt(
    esc_command(EnableCustomCharacterMode(True)),
    esc_command(EnableCustomCharacterMode(False)),
)
