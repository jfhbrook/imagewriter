from collections.abc import Callable
from contextlib import AbstractContextManager, contextmanager
from enum import Enum
import importlib.resources
from typing import Any, Generator, Self, Type

from imagewriter.base.character import MouseTextCharacter
from imagewriter.base.language import Language
from imagewriter.base.pitch import Pitch
from imagewriter.base.quality import Quality
from imagewriter.encoding import Command
from imagewriter.render import PandocRenderer, RichTextBuilder

# A markdown test page
MARKDOWN: str = importlib.resources.read_text(__name__, "./test.md")

TEST_PHRASE: str = "A quick brown fox jumped over the lazy dog"

LANGUAGE_CHARS: str = f"#${chr(64)}`\\|~[]()"

MOUSETEXT_CHARS: list[MouseTextCharacter] = [
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
    MouseTextCharacter.UPPER_RIGHT_ONE_EIGHT_BLOCK,
    MouseTextCharacter.CARRIAGE_RETURN,
    MouseTextCharacter.FULL_BLOCK,
    MouseTextCharacter.LEFTWARDS_ARROW_AND_UPPER_AND_LOWER_ONE_EIGHT_BLOCK,
    MouseTextCharacter.RIGHTWARDS_ARROW_AND_UPPER_AND_LOWER_ONE_EIGHT_BLOCK,
    MouseTextCharacter.DOWNWARDS_ARROW_AND_RIGHT_ONE_EIGHT_BLOCK,
    MouseTextCharacter.UPWARDS_ARROW_AND_RIGHT_ONE_EIGHT_BLOCK,
    MouseTextCharacter.UPPER_ONE_EIGHT_BLOCK,
    MouseTextCharacter.LEFT_AND_LOWER_ONE_EIGHT_BLOCK,
    MouseTextCharacter.RIGHTWARDS_ARROW,
    MouseTextCharacter.MEDIUM_SHADE,
    MouseTextCharacter.DARK_SHADE,
    MouseTextCharacter.LEFT_HALF_FOLDER,
    MouseTextCharacter.RIGHT_HALF_FOLDER,
    MouseTextCharacter.RIGHT_ONE_EIGHT_BLOCK,
    MouseTextCharacter.BLACK_DIAMOND,
    MouseTextCharacter.LOWER_ONE_EIGHT_BLOCK,
    MouseTextCharacter.VOIDED_GREEK_CROSS,
    MouseTextCharacter.RIGHT_OPEN_SQUARED_DOT,
    MouseTextCharacter.LEFT_ONE_EIGHT_BLOCK,
]


def enum_value_length(enum_cls: Type[Enum]) -> int:
    return max([len(e.value) for e in enum_cls])


class TestPage:
    """
    Print test pages.
    """

    def __init__(
        self: Self, rich_text_builder: RichTextBuilder, pandoc_renderer: PandocRenderer
    ) -> None:
        self.builder = rich_text_builder
        self.pandoc = pandoc_renderer

        self._standalone: bool = True

    #
    # Public methods
    #

    def full_monty(self: Self) -> list[Command]:
        """
        Print all tests.
        """

        with self._report("Test Page"):
            self._languages(standalone=False)
            self._pitch(standalone=False)
            self._quality(standalone=False)
            self._mousetext(standalone=False)
            self._markdown(standalone=False)

        return self.builder.commands

    def languages(self: Self) -> list[Command]:
        """
        Test each supported language.
        """

        self._languages(standalone=True)

        return self.builder.commands

    def pitch(self: Self) -> list[Command]:
        """
        Test each supported pitch.
        """

        self._pitch(standalone=True)

        return self.builder.commands

    def quality(self: Self) -> list[Command]:
        """
        Test each supported print quality.
        """

        self._quality(standalone=True)

        return self.builder.commands

    def attributes(self: Self) -> list[Command]:
        """
        Test various attributes, such as boldface.
        """

        self._attributes(standalone=True)

        return self.builder.commands

    def mousetext(self: Self) -> list[Command]:
        """
        Test printing mousetext characters.
        """

        self._mousetext(standalone=True)

        return self.builder.commands

    def markdown(self: Self) -> list[Command]:
        """
        Test printing markdown.
        """

        return self._markdown(standalone=True)

    #
    # Individual reports
    #

    def _languages(self: Self, standalone: bool = True) -> None:
        with self._report("Languages", standalone=standalone):
            self._enum_test(Language, LANGUAGE_CHARS, ctx=self.builder.language)

    def _pitch(self: Self, standalone: bool = True) -> None:
        with self._report("Pitch", standalone=standalone):
            self._enum_test(Pitch, TEST_PHRASE, ctx=self.builder.pitch)

    def _quality(self: Self, standalone: bool = True) -> None:
        length = len("near letter quality")

        with self._report("Quality", standalone=standalone):
            for name, quality in [
                ("draft", Quality.DRAFT),
                ("correspondence", Quality.CORRESPONDENCE),
                ("near letter quality", Quality.NEAR_LETTER_QUALITY),
            ]:
                with self.builder.line():
                    with self.builder.quality(quality):
                        with self.builder.boldface():
                            self.builder.text(f"{name:>{length}}:")
                        self.builder.text(f" {TEST_PHRASE}")

    def _attributes(self: Self, standalone: bool = True) -> None:
        attrs = [
            ("Double width", self.builder.double_width),
            ("Underlined", self.builder.underline),
            ("Boldface", self.builder.boldface),
            ("Half height", self.builder.half_height),
            ("Superscript", self.builder.superscript),
            ("Subscript", self.builder.subscript),
            ("Unslashed 0", self.builder.unslashed_zero),
            ("Slashed 0", self.builder.slashed_zero),
        ]

        with self._report("Attributes", standalone=standalone):

            with self.builder.graf():
                with self.builder.line():
                    self.builder.text("Plain")

                for name, ctx in attrs:
                    with self.builder.line():
                        with ctx():
                            self.builder.text(name)

    def _mousetext(self: Self, standalone: bool = True) -> None:
        with self._report("MouseText", standalone=standalone):
            with self.builder.graf():
                for char in MOUSETEXT_CHARS:
                    self.builder.text(char)

    def _markdown(self: Self, standalone: bool = True) -> list[Command]:
        return self.pandoc.render(MARKDOWN, format="markdown", standalone=standalone)

    #
    # Helpers
    #

    @contextmanager
    def _report(
        self: Self, name: str, standalone: bool = True
    ) -> Generator[None, None, None]:

        def title() -> None:
            with self.builder.hed(1):
                self.builder.text(name)

        if standalone:
            with self.builder.quality(Quality.NEAR_LETTER_QUALITY):
                title()

                self._hed_level = 2

                yield

                self._hed_level = 1

            self.builder.ff()
        else:
            self._standalone = False

            title()

            yield

            self._standalone = True

    def _enum_test(
        self: Self,
        enum_cls: Type[Enum],
        value: str,
        ctx: Callable[[Any], AbstractContextManager[None]],
    ) -> None:
        length = enum_value_length(enum_cls)

        for enum in enum_cls:
            with self.builder.line():
                with self.builder.boldface():
                    self.builder.text(f"{enum.value:>{length}}:")
                    with ctx(enum):
                        self.builder.text(f" {value}")
