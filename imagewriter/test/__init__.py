import importlib.resources
from typing import List, Self

from dependency_injector.wiring import inject, Provide

from imagewriter.character import MouseTextCharacter
from imagewriter.container import Container
from imagewriter.document import Document, Header, split_text
from imagewriter.encoding import (
    boldface,
    CharacterEncoder,
    Command,
    cr_lf,
    double_width,
    half_height,
    Print,
    PRINT_SLASHED_ZERO,
    PRINT_UNSLASHED_ZERO,
    set_language,
    SetPitch,
    START_SUBSCRIPT,
    START_SUPERSCRIPT,
    STOP_SUBSCRIPT,
    underline,
)
from imagewriter.language import Language
from imagewriter.pitch import Pitch
from imagewriter.render import DocumentRenderer, PandocRenderer


class TitleRenderer:
    def __init__(self: Self, renderer: DocumentRenderer) -> None:
        self._renderer = renderer

    def __call__(self: Self, title: str, level: int) -> List[Command]:
        return self._renderer.render(
            Document(blocks=[Header(level=level, contents=split_text(title))])
        )


MARKDOWN: str = importlib.resources.read_text(__name__, "./test.md")


def language_test(title: TitleRenderer) -> List[Command]:
    commands: List[Command] = list()

    for language in Language:
        commands += [
            *title(language.value, 3),
            set_language(language),
            Print(f"#${chr(64)}[\\]`(|)~".encode(encoding="ascii")),
            *cr_lf(),
        ]

    commands = commands[:-2]

    return commands


def pitch_test(title: TitleRenderer) -> List[Command]:
    commands: List[Command] = list()

    for pitch in Pitch:
        commands += [
            *title(pitch.value, 3),
            SetPitch(pitch),
            Print(b"A quick brown fox jumped over the lazy dog"),
            *cr_lf(),
        ]

    commands = commands[:-2]

    return commands


def attributes_test(encoder: CharacterEncoder) -> List[Command]:
    return [
        *encoder.encode("Plain"),
        *cr_lf(),
        *double_width(encoder.encode("Double width\r\n")),
        *cr_lf(),
        *underline(encoder.encode("Underlined\r\n")),
        *cr_lf(),
        *boldface(encoder.encode("Boldface\r\n")),
        *cr_lf(),
        *half_height(encoder.encode("Half height\r\n")),
        *cr_lf(),
        START_SUPERSCRIPT,
        *encoder.encode("Superscript\r\n"),
        *cr_lf(),
        START_SUBSCRIPT,
        *encoder.encode("Subscript\r\n"),
        *cr_lf(),
        STOP_SUBSCRIPT,
        PRINT_UNSLASHED_ZERO,
        *encoder.encode("Unslashed 0\r\n"),
        *cr_lf(),
        PRINT_SLASHED_ZERO,
        *encoder.encode("Slashed 0\r\n"),
    ]


def mousetext_test(encoder: CharacterEncoder) -> List[Command]:
    return encoder.encode(
        MouseTextCharacter.DARK_APPLE,
        MouseTextCharacter.LIGHT_APPLE,
        MouseTextCharacter.ARROWHEAD_SHAPED_POINTER,
        MouseTextCharacter.HOURGLASS,
        MouseTextCharacter.CHECK_MARK,
        MouseTextCharacter.INVERSE_CHECK_MARK,
        MouseTextCharacter.DOWNWARDS_ARROW_WITH_TIP_LEFTWARDS,
        MouseTextCharacter.TITLE_BAR,
        MouseTextCharacter.LEFTWARDS_ARROW,
        MouseTextCharacter.ELLIPSIS,
        MouseTextCharacter.DOWNWARDS_ARROW,
        MouseTextCharacter.UPWARDS_ARROW,
        MouseTextCharacter.UPPER_ONE_EIGHTS_BLOCK,
        MouseTextCharacter.CARRIAGE_RETURN,
        MouseTextCharacter.FULL_BLOCK,
        MouseTextCharacter.LEFTWARDS_ARROW_AND_UPPER_AND_LOWER_ONE_EIGHTH_BLOCK,
        MouseTextCharacter.RIGHTWARDS_ARROW_AND_UPPER_AND_LOWER_ONE_EIGHTH_BLOCK,
        MouseTextCharacter.DOWNWARDS_ARROW_AND_RIGHT_ONE_EIGHTH_BLOCK,
        MouseTextCharacter.UPWARDS_ARROW_AND_RIGHT_ONE_EIGHTH_BLOCK,
        MouseTextCharacter.ALSO_UPPER_ONE_EIGHTS_BLOCK,
        MouseTextCharacter.LEFT_AND_LOWER_ONE_EIGHTH_BLOCK,
        MouseTextCharacter.RIGHTWARDS_ARROW,
        MouseTextCharacter.BLOCK_2,
        MouseTextCharacter.BLOCK_3,
        MouseTextCharacter.LEFT_HALF_FOLDER,
        MouseTextCharacter.RIGHT_HALF_FOLDER,
        MouseTextCharacter.RIGHT_ONE_EIGHTH_BLOCK,
        MouseTextCharacter.BLACK_DIAMOND,
        MouseTextCharacter.UPPER_AND_LOWER_ONE_EIGHTH_BLOCK,
        MouseTextCharacter.VOIDED_GREEK_CROSS,
        MouseTextCharacter.RIGHT_OPEN_SQUARED_DOT,
        MouseTextCharacter.LEFT_ONE_EIGHTH_BLOCK,
    )


def markdown_test(renderer: PandocRenderer) -> List[Command]:
    return renderer.render(MARKDOWN, format="markdown")


@inject
def test_page(
    character_encoder=Provide[Container.character_encoder],
    document_renderer=Provide[Container.document_renderer],
    pandoc_renderer=Provide[Container.pandoc_renderer],
) -> List[Command]:
    title = TitleRenderer(document_renderer)
    return [
        *title("Test Page", 1),
        *title("Language", 2),
        *language_test(title),
        *title("Pitch", 2),
        *pitch_test(title),
        *cr_lf(2),
        *title("Attributes", 2),
        *attributes_test(character_encoder),
        *cr_lf(2),
        *title("MouseText", 2),
        *mousetext_test(character_encoder),
        *title("Markdown", 2),
        *markdown_test(pandoc_renderer),
    ]
