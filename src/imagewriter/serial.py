"""
Serial connectivity for the ImageWriter II.

The ImageWriter II communicates over serial with the following standard settings:

* No parity bits
* One stop bit
* DSR and DTR lines

The printer uses a baud rate of 300 bps, 1200 bps, 2400 bps, or 9600 bps. This is set
with physical DIP switches on the printer itself.
"""

# ⚠️ ACHTUNG! ⚠️
#
# You will at some point be tempted to combine this module with the `connection`
# module. You can not do this in a straightforward way because other modules depend
# on the `BaudRate` type, leading to circular import issues. Unless you are willing to
# place the `BaudRate` type in a lone module, do not attempt this.

import time
from enum import Enum
from typing import Literal, Self

import serial

BaudRate = Literal[300, 1200, 2400, 9600]
AVAILABLE_WHEN_CTS_LOW = 27
AVAILABLE_WHEN_CTS_HIGH = 100


class SerialError(Exception):
    """
    A serial port related error.
    """


class SerialProtocol(Enum):
    """
    The ImageWriter II supports two flow control protocols - hardware handshake and
    XON/XOFF. These are configured with physical DIP switches.

    The hardware handshake protocol is documented by Apple as using its DTR line. Apple
    recommends connecting its DTR and DSR lines to the serial device's DSR/DCD and DTR
    lines, respectively. This recommendation is based on an older regime, where DSR/DCD
    and DTR were abused to manage flow control a la modern RTS/CTS. On a modern system,
    DSR and DTR often can not be controlled directly at the OS level, and should not be
    used in this manner. Instead, the ImageWriter II's DTR and DSR lines should be
    wired to the serial device's RTS and CTS lines, respectively.

    When the CTS line is low (in the "hardware handshake" protocol), the print buffer
    has 27 bytes (or fewer) of space before the print buffer is completely full and
    the printer goes into an error state. The documentation suggests the true value is
    30 bytes, but up to 3 of those bytes may already be used by the time the host
    receives the signal.

    When CTS goes high (in the "hardware handshake" protocol), you are guaranteed to
    have at least 100 characters of space in the print buffer. This means that, if the
    CTS line went high from low, we can actually expect up to 70 characters before CTS
    goes low again.

    See page 193 of the ImageWriter II Technical Reference Manual
    for more details on the semantics of flow control.

    Note that the ImageWriter II expects to run in a "half-duplex" mode, where
    it waits for the RTS line to de-assert before processing the data in its
    buffer. This means that, even with hardware level RTS/CTS control, the
    RTS line should be manually de-asserted when not in use.

    The XON/XOFF flow control mode ignores the ImageWriter II's DTR/DSR lines,
    and instead communicates the same semantics using XON/XOFF control codes.

    **WARNING:** XON/XOFF has not been tested and may not work!
    """

    HARDWARE_HANDSHAKE = "Hardware Handshake"
    XONXOFF = "XON/XOFF"


class Serial(serial.Serial):
    """
    A serial connection.

    This class is a thin wrapper around pyserial's Serial class, which configures the
    ImageWriter II with standard settings and accounts for its flow control protocol
    semantics.
    """

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
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout,
            write_timeout=write_timeout,
            inter_byte_timeout=inter_byte_timeout,
            exclusive=exclusive,
            dsrdtr=True,
            rtscts=protocol == SerialProtocol.HARDWARE_HANDSHAKE,
            xonxoff=protocol == SerialProtocol.XONXOFF,
        )

        self._protocol: SerialProtocol = protocol

    @property
    def protocol(self: Self) -> SerialProtocol:
        """
        The active serial protocol.
        """
        return self._protocol

    @protocol.setter
    def protocol(self: Self, protocol: SerialProtocol) -> None:
        self._protocol = protocol
        self.rtscts = protocol == SerialProtocol.HARDWARE_HANDSHAKE
        self.xonxoff = protocol == SerialProtocol.XONXOFF

    @property
    def period(self: Self) -> float:
        """
        The amount of time in between received bytes, when the ImageWriter II is
        writing at the full baud rate.
        """
        return 1 / self.baudrate

    def tick(self: Self) -> None:
        """
        Wait for the amount of time it would take to receive a byte from the
        ImageWriter II when it's writing at its full baud rate.
        """
        time.sleep(self.period)
