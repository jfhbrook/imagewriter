from typing import Any, Generator

from parsy import alt, generate, Parser, regex, string  # type: ignore

from imagewriter.base.character import CodePoint, CustomCharacter
from imagewriter.encoding.character.language import (
    LANGUAGE_CHARACTERS,
    language_encoding,
)
from imagewriter.encoding.character.mousetext import mousetext_lookup, MOUSETEXT_LOOKUP

language_character: Parser = alt(
    *[string(char) for char in LANGUAGE_CHARACTERS.keys()]
).map(language_encoding)

mousetext_character: Parser = alt(
    *[string(name) for name in MOUSETEXT_LOOKUP.keys()]
).map(mousetext_lookup)


def to_custom_character(code: str) -> CustomCharacter:
    point: CodePoint = code
    try:
        point = int(code)
    except ValueError:
        pass

    return CustomCharacter(point)


@generate
def custom_character() -> Generator[Parser, Any, CustomCharacter]:
    begin = string(":custom_")
    end = string(":")

    character = regex(r"[^:]")
    escaped = (string("\\") >> string(":")).map(lambda s: s)

    def collect(characters: list[str]) -> str:
        return "".join(characters)

    yield begin

    code: str = (yield (escaped | character).many().map(collect))

    yield end

    return to_custom_character(code)
