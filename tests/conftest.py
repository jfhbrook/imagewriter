from typing import Callable, List
from unittest.mock import Mock

import pytest

from imagewriter.connection import Connection
from imagewriter.container import Container, SerialFactory
from imagewriter.encoding.base import Bytes, Command
from imagewriter.serial import Serial
from imagewriter.switch import DIPSwitches


@pytest.fixture
def encoded_text() -> Callable[[str | bytes], List[Command]]:
    def encoded_text(text: str | bytes) -> List[Command]:
        buffer = text if isinstance(text, bytes) else text.encode(encoding="ascii")
        return [Bytes(byte.to_bytes(byteorder="big")) for byte in buffer]

    return encoded_text


@pytest.fixture
def port() -> str:
    return "/dev/ttyUSB0"


@pytest.fixture
def serial() -> Serial:
    return Mock(name="serial")


@pytest.fixture
def serial_factory(serial: Serial) -> SerialFactory:
    def factory(port: str, dip_switches: DIPSwitches) -> Serial:
        return serial

    return factory


@pytest.fixture
def container(port, serial_factory) -> Container:
    return Container(port=port, serial=serial_factory)


@pytest.fixture
def connection(container: Container) -> Connection:
    return container.connection
