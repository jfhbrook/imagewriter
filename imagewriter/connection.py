from contextlib import contextmanager
from typing import Generator, List, Optional, Self, Sequence

from imagewriter.encoding import Command
from imagewriter.serial import Serial, SerialProtocol


class Connection:
    def __init__(self: Self, port: Serial) -> None:
        self._port: Serial = port

        self._command_buffer: List[Command] = list()
        self._bytes_buffer: Optional[bytes] = None

        self.paused: bool = False

    @property
    def port(self: Self) -> Serial:
        return self._port

    def write(self: Self, commands: Sequence[Command]) -> None:
        """
        Write to the serial port.

        Commands are buffered, respecting the ImageWriter II's CTS signal.
        """

        # TODO: Manage a buffer, respect pause
        for command in commands:
            self.port.write(bytes(command))

    @contextmanager
    def paused_writes(self: Self) -> Generator[None, None, None]:
        """
        Create a context where writes are paused.
        """

        self.paused = True

        # TODO: Wait until current command has finished writing.

        yield

        self.paused = False

    @contextmanager
    def disabled_flow_control(self: Self) -> Generator[None, None, None]:
        """
        Create a context where flow control is disabled.
        """

        self.port.rtscts = False
        self.port.xonxoff = False

        yield

        self.port.rtscts = self.port.protocol == SerialProtocol.HARDWARE_HANDSHAKE
        self.port.xonxoff = self.port.protocol == SerialProtocol.XONXOFF

    def interrupt(self: Self, commands: Sequence[Command]) -> None:
        """
        Interrupt buffered commands with new commands.
        """

        with self.paused_writes():
            with self.disabled_flow_control():
                for command in commands:
                    self.port.write(bytes(command))
