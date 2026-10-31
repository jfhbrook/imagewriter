import importlib.resources
from collections.abc import Callable, Generator
from typing import Any, Self, cast
from unittest.mock import Mock

import pytest

from imagewriter.base.settings import Settings
from imagewriter.connection import Connection
from imagewriter.container import Container
from imagewriter.encoding import (
    CR,
    LF,
    CharacterEncoder,
    Command,
    Print,
)
from imagewriter.serial import BaudRate, Serial, SerialProtocol
from imagewriter.test import TestPage as _TestPage

CHARACTER_ENCODER = CharacterEncoder()

HELLO_WORLD: list[Command] = CHARACTER_ENCODER.encode("Hello world!") + [CR, LF]

PANDOC_MARKDOWN: str = importlib.resources.read_text(
    __name__, "documents/test_pandoc.md"
)


@pytest.fixture
def encoded_text() -> Callable[[str | bytes], list[Command]]:
    def encoded_text(text: str | bytes) -> list[Command]:
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
        port: str | None = None,
        baudrate: BaudRate = 9600,
        timeout: float | None = None,
        protocol: SerialProtocol = SerialProtocol.HARDWARE_HANDSHAKE,
        write_timeout: float | None = None,
        inter_byte_timeout: float | None = None,
        exclusive: bool | None = None,
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
        cast(Any, self).write = Mock(name="Serial().write", return_value=1)
        cast(Any, self).flush = Mock(name="Serial().flush", return_value=1)

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
def container(port, serial) -> Generator[Container]:
    container = Container()

    with container.port.override(port), container.serial.override(serial):
        yield container


@pytest.fixture
def connection(container: Container) -> Generator[Connection]:
    connection = container.connection()

    yield connection

    connection.shutdown()


@pytest.fixture
def settings(container: Container) -> Settings:
    return container.settings()


@pytest.fixture
def hello_world() -> list[Command]:
    return HELLO_WORLD


@pytest.fixture
def test_page(container: Container) -> _TestPage:
    return container.test_page()


@pytest.fixture
def pandoc_markdown() -> str:
    return PANDOC_MARKDOWN
