import importlib.resources
from typing import Callable, Generator, List, Optional, Self
from unittest.mock import Mock

import pytest

from imagewriter.character import MouseTextCharacter
from imagewriter.connection import Connection
from imagewriter.container import Container
from imagewriter.encoding import (
    boldface,
    CharacterEncoder,
    Command,
    CR,
    double_width,
    half_height,
    LF,
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
from imagewriter.serial import BaudRate, Serial, SerialProtocol
from imagewriter.settings import Settings

#
# Some fixtures that may be imported directly by Jupyter notebooks.
#

CHARACTER_ENCODER = CharacterEncoder()

HELLO_WORLD: List[Command] = CHARACTER_ENCODER.encode("Hello world!") + [CR, LF]
ATTRIBUTES: List[Command] = [
    *CHARACTER_ENCODER.encode("Plain\r\n"),
    *double_width(CHARACTER_ENCODER.encode("Double width\r\n")),
    *underline(CHARACTER_ENCODER.encode("Underlined\r\n")),
    *boldface(CHARACTER_ENCODER.encode("Boldface\r\n")),
    *half_height(CHARACTER_ENCODER.encode("Half height\r\n")),
    START_SUPERSCRIPT,
    *CHARACTER_ENCODER.encode("Superscript\r\n"),
    START_SUBSCRIPT,
    *CHARACTER_ENCODER.encode("Subscript\r\n"),
    STOP_SUBSCRIPT,
    PRINT_UNSLASHED_ZERO,
    *CHARACTER_ENCODER.encode("Unslashed 0\r\n"),
    PRINT_SLASHED_ZERO,
    *CHARACTER_ENCODER.encode("Slashed 0\r\n"),
    CR,
]
SIMPLE_MARKDOWN: str = importlib.resources.read_text(
    __name__, "./documents/test_markdown.md"
)
PANDOC_MARKDOWN: str = importlib.resources.read_text(
    __name__, "documents/test_pandoc.md"
)


def _title(title: str) -> List[Command]:
    return boldface(double_width([Print(f"=== {title} ===".encode(encoding="ascii"))]))


def _language_test(language: Language) -> List[Command]:
    return [
        *boldface([Print(f"-- {language.value} --".encode(encoding="ascii"))]),
        *set_language(language),
        Print(f"#${chr(64)}[\\]`(|)~".encode(encoding="ascii")),
    ]


LANGUAGES: List[Command] = [
    *_title("Languages"),
    CR,
    LF,
    CR,
    LF,
    *_language_test(Language.AMERICAN),
    CR,
    LF,
    CR,
    LF,
    *_language_test(Language.BRITISH),
    CR,
    LF,
    CR,
    LF,
    *_language_test(Language.GERMAN),
    CR,
    LF,
    CR,
    LF,
    *_language_test(Language.FRENCH),
    CR,
    LF,
    CR,
    LF,
    *_language_test(Language.SWEDISH),
    CR,
    LF,
    CR,
    LF,
    *_language_test(Language.ITALIAN),
    CR,
    LF,
    CR,
    LF,
    *_language_test(Language.SPANISH),
    CR,
    LF,
    CR,
    LF,
    *_language_test(Language.DANISH),
]


def _pitch_test(pitch: Pitch) -> List[Command]:
    return [
        *boldface([Print(f"-- {pitch.value} --".encode(encoding="ascii"))]),
        SetPitch(pitch),
        CR,
        LF,
        CR,
        LF,
        Print(b"A quick brown fox jumped over the lazy dog"),
    ]


PITCHES: List[Command] = [
    *_title("Pitches"),
    CR,
    LF,
    CR,
    LF,
    *_pitch_test(Pitch.EXTENDED),
    CR,
    LF,
    CR,
    LF,
    *_pitch_test(Pitch.PICA),
    CR,
    LF,
    CR,
    LF,
    *_pitch_test(Pitch.ELITE),
    CR,
    LF,
    CR,
    LF,
    *_pitch_test(Pitch.SEMICONDENSED),
    CR,
    LF,
    CR,
    LF,
    *_pitch_test(Pitch.CONDENSED),
    CR,
    LF,
    CR,
    LF,
    *_pitch_test(Pitch.ULTRACONDENSED),
    CR,
    LF,
    CR,
    LF,
    *_pitch_test(Pitch.PICA_PROPORTIONAL),
    CR,
    LF,
    CR,
    LF,
    *_pitch_test(Pitch.ELITE_PROPORTIONAL),
]


MOUSETEXT = [
    _title("MouseText"),
    CR,
    LF,
    CR,
    LF,
    *CHARACTER_ENCODER.encode(
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
    ),
]


@pytest.fixture
def encoded_text() -> Callable[[str | bytes], List[Command]]:
    def encoded_text(text: str | bytes) -> List[Command]:
        buffer: bytes = (
            text if isinstance(text, bytes) else text.encode(encoding="ascii")
        )
        return [Print(byte.to_bytes(byteorder="big")) for byte in buffer]

    return encoded_text


@pytest.fixture
def port() -> str:
    return "/dev/ttyUSB0"


class MockSerial(Serial):
    def __init__(
        self: Self,
        port: Optional[str] = None,
        baudrate: BaudRate = 9600,
        timeout: Optional[float] = None,
        protocol: SerialProtocol = SerialProtocol.HARDWARE_HANDSHAKE,
        write_timeout: Optional[float] = None,
        inter_byte_timeout: Optional[float] = None,
        exclusive: Optional[bool] = None,
    ) -> None:
        super().__init__(
            port,
            baudrate,
            timeout,
            protocol,
            write_timeout,
            inter_byte_timeout,
            exclusive,
        )

        # Overrides for cts, rtscts, etc
        self._cts: bool = True
        self._rtscts: bool = protocol == SerialProtocol.HARDWARE_HANDSHAKE
        self._xonxoff: bool = protocol == SerialProtocol.XONXOFF

        # Mocked methods
        self.write = Mock(name="Serial().write")
        self.flush = Mock(name="Serial().flush")

    @property
    def cts(self: Self) -> bool:
        return self._cts

    @cts.setter
    def cts(self: Self, cts: bool) -> None:
        self._cts = cts

    @property
    def rtscts(self: Self) -> bool:
        return self._rtscts

    @rtscts.setter
    def rtscts(self: Self, rtscts: bool) -> None:
        self._rtscts = rtscts

    @property
    def xonxoff(self: Self) -> bool:
        return self._xonxoff

    @xonxoff.setter
    def xonxoff(self: Self, xonxoff: bool) -> None:
        self._xonxoff = xonxoff

    def open(self: Self) -> None:
        pass

    def close(self: Self) -> None:
        pass


@pytest.fixture
def serial(port: str) -> Serial:
    return MockSerial(port)


@pytest.fixture
def container(port, serial) -> Generator[Container, None, None]:
    container = Container()

    with container.port.override(port):
        with container.serial.override(serial):
            yield container


@pytest.fixture
def connection(container: Container) -> Generator[Connection, None, None]:
    connection = container.connection()

    yield connection

    connection.shutdown()


@pytest.fixture
def settings(container: Container) -> Settings:
    return container.settings()


@pytest.fixture
def hello_world() -> List[Command]:
    return HELLO_WORLD


@pytest.fixture
def simple_markdown() -> str:
    return SIMPLE_MARKDOWN


@pytest.fixture
def pandoc_markdown() -> str:
    return PANDOC_MARKDOWN


@pytest.fixture
def attributes() -> List[Command]:
    return ATTRIBUTES
