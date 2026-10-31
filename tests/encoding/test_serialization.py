import pytest

from imagewriter.base.character import CustomCharacter, CustomCharacterData, Language
from imagewriter.base.color import Color
from imagewriter.base.pitch import Pitch
from imagewriter.base.print import PrintCommands
from imagewriter.base.quality import Quality
from imagewriter.base.switch import SoftwareSwitch
from imagewriter.base.units import Inch
from imagewriter.encoding import (
    BACKSPACE,
    Bytes,
    CANCEL_CURRENT_LINE,
    CLEAR_ALL_TABS,
    ClearManyTabs,
    CloseSoftwareSwitches,
    Command,
    CR,
    Ctrl,
    DESELECT,
    Esc,
    FF,
    InsertSpaces,
    LF,
    LINE_FEED_FORWARD,
    LINE_FEED_REVERSE,
    LineFeed,
    OpenSoftwareSwitches,
    Print,
    PRINT_SLASHED_ZERO,
    PRINT_UNSLASHED_ZERO,
    PrintGraphicsData,
    REQUEST_SELF_IDENTIFY,
    RESET,
    SELECT,
    set_language,
    SET_TOP_OF_FORM,
    SetAutoLFAfterCR,
    SetColor,
    SetCRInsertion,
    SetDistanceBetweenLines,
    SetLeftMargin,
    SetLFWhenLineFull,
    SetLinesPerInch,
    SetManyTabs,
    SetOneTab,
    SetPageLength,
    SetPaperOutSensor,
    SetPerforationSkip,
    SetPitch,
    SetPrintCommands,
    SetQuality,
    SetSoftwareSelectResponse,
    SetSoftwareSwitches,
    SetSpacing,
    SetUnidirectionalPrinting,
    Space,
    START_BOLDFACE,
    START_DOUBLE_WIDTH,
    START_HALF_HEIGHT,
    START_SUBSCRIPT,
    START_SUPERSCRIPT,
    START_UNDERLINE,
    STOP_BOLDFACE,
    STOP_DOUBLE_WIDTH,
    STOP_HALF_HEIGHT,
    STOP_SUBSCRIPT,
    STOP_SUPERSCRIPT,
    STOP_UNDERLINE,
    TAB,
)

# TODO: Expose these in imagewriter.encoding again
from imagewriter.encoding.character.base import DISABLE_MODE
from imagewriter.encoding.character.custom import (
    EnableCustomCharacterMode,
    LoadCustomCharacters,
    SetMaxCustomCharacterWidth,
)
from imagewriter.encoding.character.mousetext import ENABLE_MOUSETEXT_MAPPING_MODE

COMMANDS: list[tuple[str, Command]] = [
    ("backspace", BACKSPACE),
    ("raw bytes", Bytes(b"hello")),
    ("cancel current line", CANCEL_CURRENT_LINE),
    ("clear all tabs", CLEAR_ALL_TABS),
    ("close many tabs", ClearManyTabs([4, 8, 12])),
    (
        "close software switches",
        CloseSoftwareSwitches({SoftwareSwitch.LANGUAGE_1, SoftwareSwitch.LANGUAGE_2}),
    ),
    ("carriage return", CR),
    ("control character", Ctrl("Q")),
    ("deselect", DESELECT),
    ("disable mode", DISABLE_MODE),
    ("enable MouseText mapping mode", ENABLE_MOUSETEXT_MAPPING_MODE),
    ("enable custom character mode", EnableCustomCharacterMode(True)),
    ("enable custom character mode with mapping", EnableCustomCharacterMode(False)),
    ("escape code", Esc("x")),
    ("form feed", FF),
    # TODO: Should this throw on non-proportional fonts?
    ("insert spaces", InsertSpaces(Pitch.ELITE_PROPORTIONAL, 2)),
    ("line feed", LF),
    ("line feed forward", LINE_FEED_FORWARD),
    ("line feed reverse", LINE_FEED_REVERSE),
    ("line feed 2 lines", LineFeed(2)),
    # TODO: Is this serialization correct?
    (
        "load custom character data",
        LoadCustomCharacters([CustomCharacterData(CustomCharacter(ord("a")), b"1234")]),
    ),
    (
        "open software switches",
        OpenSoftwareSwitches({SoftwareSwitch.LANGUAGE_1, SoftwareSwitch.LANGUAGE_2}),
    ),
    ("print hello", Print(b"hello")),
    ("print slashed zero", PRINT_SLASHED_ZERO),
    ("print unslashed zero", PRINT_UNSLASHED_ZERO),
    ("print graphics data", PrintGraphicsData(b"1234")),
    ("request self-identify", REQUEST_SELF_IDENTIFY),
    ("reset", RESET),
    ("select", SELECT),
    ("set top of form", SET_TOP_OF_FORM),
    ("enable auto line feed after carriage return", SetAutoLFAfterCR(True)),
    ("disable auto line feed after carriage return", SetAutoLFAfterCR(False)),
    ("set color", SetColor(Color.BLACK)),
    ("enable carriage return insertion", SetCRInsertion(True)),
    ("disable carriage return insertion", SetCRInsertion(False)),
    ("set distance between lines", SetDistanceBetweenLines(6)),
    ("set left margin with int", SetLeftMargin(12, Pitch.ELITE)),
    ("set left margin with inch", SetLeftMargin(Inch(1), Pitch.ELITE)),
    *[
        (f"set language {n}", command)
        for n, command in enumerate(set_language(Language.BRITISH))
    ],
    ("enable line feed when line full", SetLFWhenLineFull(True)),
    ("disable line feed when line full", SetLFWhenLineFull(False)),
    ("set 6 lines per inch", SetLinesPerInch(6)),
    ("set 8 lines per inch", SetLinesPerInch(8)),
    ("set many tabs", SetManyTabs([4, 8, 12])),
    ("set custom character width to 8", SetMaxCustomCharacterWidth(8)),
    ("set custom character width to 16", SetMaxCustomCharacterWidth(16)),
    ("set one tab", SetOneTab(16)),
    ("set page length to 12", SetPageLength(12)),
    ("set page length to 11", SetPageLength(Inch(11))),
    ("enable paper out sensor", SetPaperOutSensor(True)),
    ("disable paper out sensor", SetPaperOutSensor(False)),
    ("enable perforation skip", SetPerforationSkip(True)),
    ("disable perforation skip", SetPerforationSkip(False)),
    ("set pitch", SetPitch(Pitch.ELITE)),
    (
        "set print commands to CR, LF and FF",
        SetPrintCommands(PrintCommands.CR_LF_AND_FF),
    ),
    ("set print commands to CR only", SetPrintCommands(PrintCommands.CR_ONLY)),
    ("set quality", SetQuality(Quality.NEAR_LETTER_QUALITY)),
    ("enable software select response", SetSoftwareSelectResponse(True)),
    ("disable software select response", SetSoftwareSelectResponse(False)),
    (
        "set closed software switches",
        SetSoftwareSwitches(
            True, {SoftwareSwitch.LANGUAGE_1, SoftwareSwitch.LANGUAGE_2}
        ),
    ),
    (
        "set open software switches",
        SetSoftwareSwitches(
            False, {SoftwareSwitch.LANGUAGE_1, SoftwareSwitch.LANGUAGE_2}
        ),
    ),
    # TODO: Should this throw on non-proportional fonts?
    ("set spacing", SetSpacing(Pitch.ELITE_PROPORTIONAL, 2)),
    ("enable unidirectional printing", SetUnidirectionalPrinting(True)),
    ("disable unidirectional printing", SetUnidirectionalPrinting(False)),
    ("space", Space()),
    ("start boldface", START_BOLDFACE),
    ("start double width", START_DOUBLE_WIDTH),
    ("start half height", START_HALF_HEIGHT),
    ("start subscript", START_SUBSCRIPT),
    ("start superscript", START_SUPERSCRIPT),
    ("start underline", START_UNDERLINE),
    ("stop boldface", STOP_BOLDFACE),
    ("stop double width", STOP_DOUBLE_WIDTH),
    ("stop half height", STOP_HALF_HEIGHT),
    ("stop subscript", STOP_SUBSCRIPT),
    ("stop superscript", STOP_SUPERSCRIPT),
    ("stop underline", STOP_UNDERLINE),
    ("tab", TAB),
]


@pytest.mark.parametrize("name,command", COMMANDS)
def test_bytes_command(name, command, snapshot) -> None:
    result = bytes(command)
    try:
        result.decode("utf-8") == snapshot
    except UnicodeDecodeError:
        assert result == snapshot


@pytest.mark.parametrize("name,command", COMMANDS)
def test_repr_command(name, command, snapshot) -> None:
    assert repr(command) == snapshot
