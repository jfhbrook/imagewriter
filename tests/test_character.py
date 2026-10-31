from collections.abc import Callable

import pytest

from imagewriter.base.character import (
    CodePointError,
    CustomCharacter,
    Language,
    LanguageCharacter,
    MouseTextCharacter,
    assert_ascii,
    assert_high_ascii,
    assert_low_ascii,
    repr_code_point,
)
from imagewriter.encoding.character.language import (
    LANGUAGE_CHARACTERS,
)
from imagewriter.encoding.character.mousetext import (
    MOUSETEXT_CODE_LOOKUP,
    MOUSETEXT_LOOKUP,
)
from imagewriter.encoding.character.parser import (
    custom_character,
    language_character,
    mousetext_character,
    parse_text,
)
from imagewriter.test.page import TEST_PHRASE


@pytest.mark.parametrize(
    "point", [1, "a".encode("ascii")[0], 126, 150, 160, 239, 250]
)  # "a"
def test_repr_code_point(point: int, snapshot) -> None:
    assert repr_code_point(point) == snapshot


@pytest.mark.parametrize(
    "point,assertion,passes",
    [
        (1, assert_low_ascii, False),
        (1, assert_high_ascii, False),
        (1, assert_ascii, False),
        (32, assert_low_ascii, True),
        (32, assert_high_ascii, False),
        (32, assert_ascii, True),
        (126, assert_low_ascii, True),
        (126, assert_high_ascii, False),
        (126, assert_ascii, True),
        (150, assert_low_ascii, False),
        (150, assert_high_ascii, False),
        (150, assert_ascii, False),
        (160, assert_low_ascii, False),
        (160, assert_high_ascii, True),
        (160, assert_ascii, True),
        (239, assert_low_ascii, False),
        (239, assert_high_ascii, True),
        (239, assert_ascii, True),
        (250, assert_low_ascii, False),
        (250, assert_high_ascii, False),
        (250, assert_ascii, False),
    ],
)
def test_code_point_assertions(
    point: int, assertion: Callable[[int], None], passes: bool, snapshot
) -> None:

    if passes:
        assertion(point)
        return

    with pytest.raises(CodePointError) as exc_info:
        assertion(point)

    assert str(exc_info.value) == snapshot


@pytest.mark.parametrize(
    "character", list(MOUSETEXT_LOOKUP.keys()) + list(MOUSETEXT_CODE_LOOKUP.keys())
)
def test_mousetext_character(character: str, snapshot) -> None:
    result = mousetext_character(True).parse(character)

    assert isinstance(result, list)
    for char in result:
        assert isinstance(char, MouseTextCharacter)
    assert result == snapshot


@pytest.mark.parametrize("character", list(MOUSETEXT_LOOKUP.keys()))
def test_mousetext_character_no_emoji(character: str, snapshot) -> None:
    result = mousetext_character(False).parse(character)

    assert isinstance(result, list)
    for char in result:
        assert isinstance(char, MouseTextCharacter)
    assert result == snapshot


@pytest.mark.parametrize("character", LANGUAGE_CHARACTERS.keys())
def test_language_character(character: str, snapshot) -> None:
    result = language_character.parse(character)

    assert len(result) == 1

    assert isinstance(result[0], LanguageCharacter)

    assert result[0] == snapshot


@pytest.mark.parametrize(
    "character", [":custom_a:", ":custom_32:", ":custom_160:", ":custom_\\::"]
)
def test_custom_character(character: str, snapshot) -> None:
    result = custom_character.parse(character)

    assert len(result) == 1

    assert isinstance(result[0], CustomCharacter)

    assert result[0] == snapshot


@pytest.mark.parametrize(
    "text,encode_emoji",
    [
        # MouseText
        (":folder:", True),
        (":folder:", False),
        ("█", True),
        ("█", False),
        # Language
        ("£", True),
        ("£", False),
        # Custom
        (":custom_160:", True),
        (":custom_160:", False),
        # Plain text
        (TEST_PHRASE, True),
        (TEST_PHRASE, False),
        # Mixed
        (f"{TEST_PHRASE} :folder: £", True),
        (f"{TEST_PHRASE} :folder: £", False),
        # Structured
        (
            [
                f"{TEST_PHRASE} :folder: £",
                MouseTextCharacter.DARK_APPLE,
                LanguageCharacter(language=Language.BRITISH, encoded="#"),
                CustomCharacter("a"),
                TEST_PHRASE,
            ],
            True,
        ),
        (
            [
                f"{TEST_PHRASE} :folder: £",
                MouseTextCharacter.DARK_APPLE,
                LanguageCharacter(language=Language.BRITISH, encoded="#"),
                CustomCharacter("a"),
                TEST_PHRASE,
            ],
            False,
        ),
        # Known Edge Cases
        ("foo:", True),
        ("foo:", False),
    ],
)
def test_text_parser(text: str, encode_emoji: bool, snapshot) -> None:
    assert parse_text(text, encode_emoji) == snapshot
