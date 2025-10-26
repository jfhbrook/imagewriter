import importlib.resources
from typing import Callable, Generator, List, Optional, Self
from unittest.mock import Mock

import pytest

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
    START_SUBSCRIPT,
    START_SUPERSCRIPT,
    STOP_SUBSCRIPT,
    underline,
)
from imagewriter.language import Language
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


def _language_characters(language: Language) -> List[Command]:
    return [
        *boldface([Print(f"-- {language.value} --".encode(encoding="ascii"))]),
        *set_language(language),
        Print(f"#${chr(64)}[\\]`(|)~".encode(encoding="ascii")),
    ]


LANGUAGE_CHARACTERS: List[Command] = [
    *boldface(double_width(CHARACTER_ENCODER.encode("=== Language Characters ==="))),
    CR,
    LF,
    *_language_characters(Language.AMERICAN),
    CR,
    LF,
    *_language_characters(Language.BRITISH),
    CR,
    LF,
    *_language_characters(Language.GERMAN),
    CR,
    LF,
    *_language_characters(Language.FRENCH),
    CR,
    LF,
    *_language_characters(Language.SWEDISH),
    CR,
    LF,
    *_language_characters(Language.ITALIAN),
    CR,
    LF,
    *_language_characters(Language.SPANISH),
    CR,
    LF,
    *_language_characters(Language.DANISH),
    CR,
    LF,
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
