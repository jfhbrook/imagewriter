import pytest

from imagewriter.base.character import MouseTextCharacter
from imagewriter.base.language import Language
from imagewriter.encoding.character.language import (
    language_character,
    LANGUAGE_CHARACTERS,
)
from imagewriter.encoding.character.mousetext import (
    mousetext_character,
    MOUSETEXT_LOOKUP,
)


@pytest.mark.parametrize("character", MOUSETEXT_LOOKUP.keys())
def test_mousetext_character(character: str, snapshot) -> None:
    result = mousetext_character.parse(character)

    assert isinstance(result, list)
    for character in result:
        assert isinstance(character, MouseTextCharacter)
    assert result == snapshot


@pytest.mark.parametrize("character", LANGUAGE_CHARACTERS.keys())
def test_language_character(character: str, snapshot) -> None:
    result = language_character.parse(character)

    assert isinstance(result, tuple)

    language, encoding = result

    assert isinstance(language, Language)
    assert isinstance(encoding, str)

    assert result == snapshot
