from parsy import alt, Parser, string  # type: ignore

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
