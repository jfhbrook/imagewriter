from typing import Any, Generator

from parsy import alt, generate, Parser, regex, string  # type: ignore

from imagewriter.base.character import (
    CodePoint,
    CustomCharacter,
    LanguageCharacter,
    MouseTextCharacter,
)
from imagewriter.encoding.character.language import (
    LANGUAGE_CHARACTERS,
    language_encoding,
)
from imagewriter.encoding.character.mousetext import mousetext_lookup, MOUSETEXT_LOOKUP

#
# Language encoded character
#

language_character: Parser = alt(
    *[string(char) for char in LANGUAGE_CHARACTERS.keys()]
).map(language_encoding)

#
# MouseText character
#

mousetext_character: Parser = alt(
    *[string(name) for name in MOUSETEXT_LOOKUP.keys()]
).map(mousetext_lookup)

#
# Custom character
#


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
    escaped = string("\\") >> string(":")

    yield begin

    code: str = yield (escaped | character).many().concat()

    yield end

    return to_custom_character(code)
