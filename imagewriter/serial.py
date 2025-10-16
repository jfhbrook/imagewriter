from enum import Enum
from typing import Literal, Optional, Self

import serial

BaudRate = Literal[300] | Literal[1200] | Literal[2400] | Literal[9600]

# When CTS goes low, you have 27 characters of grace before the print buffer is
# completely full and the printer goes into an error state.
#
# The documentation suggests the true value is 30 bytes, but up to 3 of those
# bytes may already be used by the time the host receives the signal.
#
# See page 193 of the ImageWriter II Technical Reference Manual for more
# details.
AVAILABLE_WHEN_CTS_LOW = 27

# When CTS goes high, you are guaranteed to have at least 100 characters. Note
# that this means we can actually expect up to 70 characters before CTS goes
# low again - and, presumably, only 97 characters given the 3 byte grace
# period.
#
# See page 193 of the ImageWriter II Technical Reference Manual for more
# details.
AVAILABLE_WHEN_CTS_HIGH = 100


class SerialProtocol(Enum):
    """
    The ImageWriter II supports two flow contrl protocols - hardware handshake
    and XON/XOFF.

    The hardware handshake protocol is documented by Apple as using its DTR
    line. Apple recommends, connecting its DTR and DSR lines to the serial
    device's DSR/DCD and DTR lines, respectively. This recommendation is based
    on an older regime, where DSR/DCD and DTR were abused to manage flow
    control a la modern RTS/CTS. On a modern system, DSR and DTR often can not
    be controlled directly at the OS level, and should not be used in this
    manner. Instead, the ImageWriter II's DTR and DSR lines should be wired to
    the serial device's RTS and CTS lines, respectively.

    Note that the ImageWriter II expects to run in a "half-duplex" mode, where
    it waits for the RTS line to de-assert before processing the data in its
    buffer. This means that, even with hardware level RTS/CTS control, the
    RTS line should be manually de-asserted when not in use.

    The XON/XOFF flow control mode ignores the ImageWriter II's DTR/DSR lines,
    and instead communicates the same semantics using XON/XOFF control codes.

    **WARNING:** XON/XOFF has not been tested and may not work!
    """

    HARDWARE_HANDSHAKE = "HARDWARE_HANDSHAKE"
    XONXOFF = "XON/XOFF"


class Serial(serial.Serial):
    """
    A serial connection supporting the particular semantics of the ImageWriter
    II. In particular, it attempts to de-assert the RTS line (or accomplish
    similar ends with XON/XOFF) when data is not being sent.
    """

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
            rtscts=False,
            xonxoff=False,
        )

        self._protocol: SerialProtocol = protocol
