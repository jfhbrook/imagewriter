from typing import Any, Self

from parsy import alt, Parser, string  # type: ignore

from imagewriter.base.language import Language
from imagewriter.encoding.base import Command
from imagewriter.encoding.character.base import Mode
from imagewriter.encoding.language import set_language

LanguageEncoding = tuple[Language, str]

# TODO: Print a test page of alternate language characters, figure out what
# the alternate characters are, and complete this table.

LANGUAGE_ENCODINGS: dict[Language, dict[str, str]] = {
    Language.AMERICAN: dict(),
    Language.BRITISH: {"£": "#"},
    Language.GERMAN: dict(),
    Language.FRENCH: dict(),
    Language.SWEDISH: dict(),
    Language.ITALIAN: dict(),
    Language.SPANISH: dict(),
    Language.DANISH: dict(),
}

LANGUAGE_CHARACTERS: dict[str, list[Language]] = {"£": [Language.BRITISH]}


def map_character(character: str) -> LanguageEncoding:
    language = LANGUAGE_CHARACTERS[character][0]
    encoded: str = LANGUAGE_ENCODINGS[language][character]

    return language, encoded


language_character: Parser = alt(
    *[string(char) for char in LANGUAGE_CHARACTERS.keys()]
).map(map_character)


class LanguageMode(Mode):
    def __init__(self: Self, language: Language) -> None:
        self.language: Language = language

    def enable(self: Self) -> list[Command]:
        return set_language(self.language)

    def disable(self: Self) -> list[Command]:
        # Language modes can not be disabled
        return []

    def __eq__(self: Self, other: Any) -> bool:
        return isinstance(other, LanguageMode) and self.language == other.language


LANGUAGE_MODES: dict[str, list[LanguageMode]] = {
    ch: [LanguageMode(lang) for lang in langs]
    for ch, langs in LANGUAGE_CHARACTERS.items()
}
