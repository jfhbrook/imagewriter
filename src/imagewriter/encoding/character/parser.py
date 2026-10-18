from typing import Any, Generator

from parsy import alt, any_char, generate, Parser, regex, string  # type: ignore

from imagewriter.base.character import (
    Character,
    CodePoint,
    CustomCharacter,
    Text,
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
).map(lambda s: [language_encoding(s)])

#
# MouseText character
#


def mousetext_character(encode_emoji: bool = True) -> Parser:
    return alt(*[string(name) for name in MOUSETEXT_LOOKUP.keys()]).map(
        mousetext_lookup
    )


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
def custom_character() -> Generator[Parser, Any, list[CustomCharacter]]:
    begin = string(":custom_")
    end = string(":")

    character = regex(r"[^:]")
    escaped = string("\\") >> string(":")

    yield begin

    code: str = yield (escaped | character).many().concat()

    yield end

    return [to_custom_character(code)]


#
# Combined parser
#


def collect(parsed: list[list[Character]]) -> list[Character]:
    return [character for chunk in parsed for character in chunk]


def code_parser(emoji_codes: bool) -> Parser:
    parser = language_character | mousetext_character(emoji_codes)
    if emoji_codes:
        parser = parser | custom_character | regex(r"[^:]")
    parser = parser | any_char

    return parser.many().map(collect)


def parse_text(text: Text, emoji_codes: bool) -> list[Character]:
    """
    Parse text into a list of characters. When `emoji_codes` is True, parse
    Slack-like emoji codes.
    """

    if isinstance(text, list):
        return [
            character for chunk in text for character in _parse_text(chunk, emoji_codes)
        ]
    return _parse_text(text, emoji_codes)


def _parse_text(text: Character, emoji_codes: bool) -> list[Character]:
    if isinstance(text, str) and emoji_codes:
        return code_parser(emoji_codes).parse(text)

    return [text]
