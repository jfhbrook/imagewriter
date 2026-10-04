import importlib.resources

from imagewriter.base.character import MouseTextCharacter
from imagewriter.base.language import Language
from imagewriter.base.pitch import Pitch
from imagewriter.base.quality import Quality
from imagewriter.encoding import Command
from imagewriter.render import PandocRenderer, RichTextBuilder

# A markdown test page
MARKDOWN: str = importlib.resources.read_text(__name__, "./test.md")


def language_test(builder: RichTextBuilder) -> None:
    """
    Test each supported language.
    """

    with builder.header(2):
        builder.text("Language")

    for language in Language:
        with builder.header(3):
            builder.text(language.value)

        with builder.language(language):
            builder.text(f"#${chr(64)}[\\]`(|)~")


def pitch_test(builder: RichTextBuilder) -> None:
    """
    Test each supported pitch.
    """

    with builder.header(2):
        builder.text("Pitch")

    for pitch in Pitch:
        with builder.header(3):
            builder.text(pitch.value)

        with builder.pitch(pitch):
            builder.text("A quick brown fox jumped over the lazy dog")


def quality_test(builder: RichTextBuilder) -> None:
    """
    Test each supported print quality.
    """

    with builder.header(2):
        builder.text("Quality")

    for name, quality in [
        ("correspondence", Quality.CORRESPONDENCE),
        ("draft", Quality.DRAFT),
        ("near letter quality", Quality.NEAR_LETTER_QUALITY),
    ]:
        with builder.header(3):
            builder.text(name)

        with builder.quality(quality):
            builder.text("A quick brown fox jumped over the lazy dog")


def attributes_test(builder: RichTextBuilder) -> None:
    """
    Test various attributes, such as boldface.
    """

    with builder.header(2):
        builder.text("Attributes")

    builder.text("Plain")
    builder.cr_lf()

    with builder.double_width():
        builder.text("Double width")
        builder.cr_lf()

    builder.cr_lf()

    with builder.underline():
        builder.text("Underlined")
        builder.cr_lf()

    builder.cr_lf()

    with builder.boldface():
        builder.text("Boldface")
        builder.cr_lf()

    builder.cr_lf()

    with builder.half_height():
        builder.text("Half height")
        builder.cr_lf()

    builder.cr_lf()

    with builder.superscript():
        builder.text("Superscript")
        builder.cr_lf()

    builder.cr_lf()

    with builder.subscript():
        builder.text("Subscript")
        builder.cr_lf()

    builder.cr_lf()

    with builder.unslashed_zero():
        builder.text("Unslashed 0")
        builder.cr_lf()

    builder.cr_lf()

    with builder.slashed_zero():
        builder.text("Slashed 0")
        builder.cr_lf()

    builder.cr_lf()


def mousetext_test(builder: RichTextBuilder) -> None:
    """
    Test printing mousetext characters.
    """

    for char in [
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
    ]:
        builder.text(char)


def markdown_test(renderer: PandocRenderer) -> list[Command]:
    return renderer.render(MARKDOWN, format="markdown")


def test_page(
    rich_text_builder: RichTextBuilder,
    pandoc_renderer: PandocRenderer,
) -> list[Command]:
    with rich_text_builder.quality(Quality.CORRESPONDENCE):
        with rich_text_builder.header(1):
            rich_text_builder.text("Test Page")

        language_test(rich_text_builder)
        pitch_test(rich_text_builder)
        quality_test(rich_text_builder)
        attributes_test(rich_text_builder)
        mousetext_test(rich_text_builder)

        commands = rich_text_builder.commands
        commands += markdown_test(pandoc_renderer)

    return commands
