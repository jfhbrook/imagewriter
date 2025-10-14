from collections.abc import Buffer
from enum import Enum
from typing import Any, Dict, Literal, Optional, Self

import serial

BaudRate = Literal[300] | Literal[1200] | Literal[2400] | Literal[9600]
Data = str | bytes


class FlowControlMode(Enum):
    """
    The ImageWriter II supports two flow control modes - hardware and XON/XOFF.

    The hardware flow control is documented by Apple as using its DTR line.
    Apple recommends, connecting its DTR and DSR lines to the serial device's
    DSR/DCD and DTR lines, respectively. This recommendation is based on an
    older regime, where DSR/DCD and DTR were abused to manage flow control a
    la modern RTS/CTS. On a modern system, DSR and DTR often can not be
    controlled directly at the OS level, and should not be used in this manner.
    Instead, the ImageWriter II's DTR and DSR lines should be wired to the
    serial device's RTS and CTS lines, respectively.

    Note that the ImageWriter II expects to run in a "half-duplex" mode, where
    it waits for the RTS line to de-assert before processing the data in its
    buffer. This means that, even with hardware level RTS/CTS control, the
    RTS line should be manually de-asserted when not in use.

    The XON/XOFF flow control mode ignores the ImageWriter II's DTR/DSR lines,
    and instead communicates the same semantics using XON/XOFF control codes.

    **WARNING:** XON/XOFF has not been tested and may not work!
    """

    RTSCTS = "RTS/CTS"
    XONXOFF = "XON/XOFF"

    @property
    def serial_kwargs(self: Self) -> Dict[str, Any]:
        return dict(
            rtscts=self != FlowControlMode.XONXOFF,
            xonxoff=self == FlowControlMode.XONXOFF,
        )


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
        flow_control: FlowControlMode = FlowControlMode.RTSCTS,
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
            **flow_control.serial_kwargs,
        )

        self._flow_control: FlowControlMode = flow_control

        # Deassert RTS when not in use
        if flow_control == FlowControlMode.RTSCTS:
            self.rts = False

    def _set_rts(self: Self, enable: bool) -> None:
        if self._flow_control == FlowControlMode.RTSCTS:
            self.rts = enable
        else:
            self.set_input_flow_control(enable)

    def open(self: Self) -> None:
        super().open()

        self._set_rts(False)

    def write(self: Self, data: Buffer) -> Optional[int]:
        # OS would likely assert RTS on write, but just in case...
        self._set_rts(True)

        rv: Optional[int] = super().write(data)

        # OS will not de-assert RTS unless data is being read, so we do it
        # here
        self._set_rts(False)

        return rv
