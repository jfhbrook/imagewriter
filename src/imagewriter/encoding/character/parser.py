from typing import Any, Generator

from parsy import (  # type: ignore
    alt,
    any_char,
    generate,
    ParseError,
    Parser,
    regex,
    string,
)

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
from imagewriter.encoding.character.mousetext import (
    MOUSETEXT_CODE_LOOKUP,
    mousetext_lookup,
    MOUSETEXT_LOOKUP,
)


class CharacterParseError(Exception):
    """
    An error when parsing characters.
    """


#
# Language encoded character
#

language_character: Parser = alt(
    *[string(char) for char in LANGUAGE_CHARACTERS.keys()]
).map(lambda s: [language_encoding(s)])

#
# MouseText character
#


def mousetext_character(encode_emoji: bool) -> Parser:
    parsers = [string(name) for name in MOUSETEXT_LOOKUP.keys()]

    if encode_emoji:
        parsers += [string(name) for name in MOUSETEXT_CODE_LOOKUP.keys()]
    return alt(*parsers).map(mousetext_lookup)


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


code_parser: Parser = (
    alt(language_character, mousetext_character(True), custom_character, any_char)
    .many()
    .map(collect)
)

non_code_parser: Parser = alt(
    language_character, mousetext_character(False), any_char
).many()


def _get_parser(emoji_codes: bool) -> Parser:
    return code_parser if emoji_codes else non_code_parser


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
    if isinstance(text, str):
        try:
            return _get_parser(emoji_codes).parse(text)
        except ParseError as exc:
            raise CharacterParseError(f"Failed to parse {text!r}") from exc

    return [text]
