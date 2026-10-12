import pytest

from imagewriter.base.character import CustomCharacter, MouseTextCharacter
from imagewriter.base.language import Language
from imagewriter.encoding.character.language import (
    LANGUAGE_CHARACTERS,
)
from imagewriter.encoding.character.mousetext import (
    MOUSETEXT_LOOKUP,
)
from imagewriter.encoding.character.parser import (
    custom_character,
    language_character,
    mousetext_character,
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


@pytest.mark.parametrize(
    "character", [":custom_a:", ":custom_32:", ":custom_160:", ":custom_\\::"]
)
def test_custom_character(character: str, snapshot) -> None:
    result = custom_character.parse(character)

    assert isinstance(result, CustomCharacter)

    assert result == snapshot
