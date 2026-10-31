from typing import Any, Self

from imagewriter.base.character import Language, LanguageCharacter
from imagewriter.encoding.base import Command
from imagewriter.encoding.character.base import Mode
from imagewriter.encoding.language import set_language

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

# Multiple languages can support the same character. In practice, we just choose one.
LANGUAGE_CHARACTERS: dict[str, list[Language]] = {"£": [Language.BRITISH]}


def language_encoding(character: str) -> LanguageCharacter:
    """
    Get the language and the encoding for a language-supported character.
    """

    language = LANGUAGE_CHARACTERS[character][0]
    encoded: str = LANGUAGE_ENCODINGS[language][character]

    return LanguageCharacter(language=language, encoded=encoded)


class LanguageMode(Mode):
    """
    A language mode.
    """

    # TODO: Set default language?
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
