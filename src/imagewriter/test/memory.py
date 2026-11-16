from imagewriter.connection import Connection
from imagewriter.encoding import CANCEL_CURRENT_LINE, CR, Print, SetLFWhenLineFull
from imagewriter.serial import Serial


def test_memory(serial: Serial, connection: Connection, print_buffer_size: int) -> int:
    connection.write([SetLFWhenLineFull(False), CR])

    i = 0

    while serial.cts and i <= 2 * print_buffer_size:
        connection.write([Print(b"x")])
        i += 1

    connection.interrupt([CANCEL_CURRENT_LINE, CR])

    return i
