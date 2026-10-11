from parsy import alt, Parser, string  # type: ignore

from imagewriter.base.language import Language

LanguageEncoding = tuple[Language, str]

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
