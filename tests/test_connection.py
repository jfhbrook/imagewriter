import time
from typing import Any
from unittest.mock import call

from imagewriter.connection import Connection
from imagewriter.encoding.base import Print


def test_connection(serial: Any, connection: Connection) -> None:
    def sleep(n: float) -> None:
        time.sleep(2 * n * connection.serial.period)

    first = Print(b"first")
    second = Print(b"second")
    interrupt = Print(b"interrupt")

    serial.cts = True

    connection.write([first])

    sleep(1)

    serial.cts = False

    connection.write([second])
    connection.interrupt([interrupt])

    sleep(2)

    serial.cts = True

    serial.write.assert_has_calls([call(bytes(first)), call(bytes(interrupt))])
