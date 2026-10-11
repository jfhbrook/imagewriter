import pytest

from imagewriter.base.character import MouseTextCharacter
from imagewriter.encoding.character.mousetext import (
    mousetext_character,
    MOUSETEXT_LOOKUP,
)


@pytest.mark.parametrize("character", MOUSETEXT_LOOKUP.keys())
def test_mousetext_character(character, snapshot) -> None:
    result = mousetext_character.parse(character)

    assert isinstance(result, list)
    for character in result:
        assert isinstance(character, MouseTextCharacter)
    assert result == snapshot
