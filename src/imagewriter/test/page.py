import importlib.resources

from imagewriter.base.character import MouseTextCharacter
from imagewriter.base.language import Language
from imagewriter.base.pitch import Pitch
from imagewriter.base.quality import Quality
from imagewriter.encoding import Command, FF
from imagewriter.render import PandocRenderer, RichTextBuilder

# A markdown test page
MARKDOWN: str = importlib.resources.read_text(__name__, "./test.md")

LANGUAGE_TABLE: list[tuple[str, str]] = [
    ("pound", "#"),
    ("dollar", "$"),
    ("at", chr(64)),
    ("left bracket", "["),
    ("backslash", "\\"),
    ("right bracket", "]"),
    ("left parenthesis", "("),
    ("right parenthesis", ")"),
    ("pipe", "|"),
    ("tilde", "~"),
]


def language_table(builder: RichTextBuilder) -> None:
    length = max([len(name) for name, _ in LANGUAGE_TABLE])

    for name, char in LANGUAGE_TABLE:
        builder.text(f"{name:>{length}} - {char}")
        builder.cr_lf()


def language_test(builder: RichTextBuilder) -> None:
    """
    Test each supported language.
    """

    with builder.hed(2):
        builder.text("Language")

    for language in Language:
        with builder.hed(3):
            builder.text(language.value)

        with builder.graf():
            with builder.language(language):
                language_table(builder)


def pitch_test(builder: RichTextBuilder) -> None:
    """
    Test each supported pitch.
    """

    with builder.hed(2):
        builder.text("Pitch")

    for pitch in Pitch:
        with builder.hed(3):
            builder.text(pitch.value)

        with builder.pitch(pitch):
            with builder.graf():
                builder.text("A quick brown fox jumped over the lazy dog")


def quality_test(builder: RichTextBuilder) -> None:
    """
    Test each supported print quality.
    """

    with builder.hed(2):
        builder.text("Quality")

    for name, quality in [
        ("draft", Quality.DRAFT),
        ("correspondence", Quality.CORRESPONDENCE),
        ("near letter quality", Quality.NEAR_LETTER_QUALITY),
    ]:
        with builder.hed(3):
            builder.text(name)

        with builder.quality(quality):
            with builder.graf():
                builder.text("A quick brown fox jumped over the lazy dog")


def attributes_test(builder: RichTextBuilder) -> None:
    """
    Test various attributes, such as boldface.
    """

    attrs = [
        ("Double width", builder.double_width),
        ("Underlined", builder.underline),
        ("Boldface", builder.boldface),
        ("Half height", builder.half_height),
        ("Superscript", builder.superscript),
        ("Subscript", builder.subscript),
        ("Unslashed zero", builder.unslashed_zero),
        ("Slashed zero", builder.slashed_zero),
    ]

    with builder.hed(2):
        builder.text("Attributes")

    with builder.graf():
        with builder.line():
            builder.text("Plain")

        for name, ctx in attrs:
            with builder.line():
                with ctx():
                    builder.text(name)


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
        with builder.line():
            builder.text(char)


def markdown_test(renderer: PandocRenderer) -> list[Command]:
    return renderer.render(MARKDOWN, format="markdown")


def test_page(
    rich_text_builder: RichTextBuilder,
    pandoc_renderer: PandocRenderer,
) -> list[Command]:
    with rich_text_builder.quality(Quality.NEAR_LETTER_QUALITY):
        with rich_text_builder.hed(1):
            rich_text_builder.text("Test Page")

        language_test(rich_text_builder)
        pitch_test(rich_text_builder)
        quality_test(rich_text_builder)
        attributes_test(rich_text_builder)
        mousetext_test(rich_text_builder)

        commands = rich_text_builder.commands
        commands += markdown_test(pandoc_renderer)
        commands.append(FF)

    return commands
