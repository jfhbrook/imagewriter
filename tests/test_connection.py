from typing import Any

import pytest

from imagewriter.connection import Connection, InterruptError
from imagewriter.encoding.base import Print


def test_connection(serial: Any, connection: Connection) -> None:
    first = Print(b"first")
    second = Print(b"second")
    interrupt = Print(b"interrupt")

    connection.write([first]).result()

    serial.cts = False

    interrupt_fut = connection.interrupt([interrupt])
    write_fut = connection.write([second])

    interrupt_fut.result()

    with pytest.raises(InterruptError):
        write_fut.result()
