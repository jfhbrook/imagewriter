"""
Connection management for the ImageWriter II.

The ImageWriter II has a number of idiosyncracies when it comes to connection
management. Namely, the ImageWriter II uses the CTS line to signal if the write buffer
is **close** to full.

The intended standard behavior is that the client should wait for the printer to flush
its buffer and signal that it's ready for more commands by dropping the CTS signal.

However, it may be necessary to send a command that *doesn't* respect the CTS line to
the printer to trigger behavior, under the assumption that there's a small overhead in
buffer space. For example, sending a CR could trigger the printer to print and flush
the buffer; or a reset command could remove buffered commands and allow for starting
over.

The `Connection` class handles this by sending discrete `Command`s to the printer
normally, respecting the CTS line; but with the capability of sending other commands
as "interrupt" commands.

For more information, review the documentation of the `Connection` object.
"""

from concurrent.futures import Executor
import logging
import queue
import time
from typing import List, Self, Sequence

from imagewriter.encoding import Command
from imagewriter.serial import Serial, SerialProtocol

logger = logging.getLogger(__name__)


class Interrupt:
    def __init__(self: Self, commands: List[Command], dump: bool) -> None:
        self.commands: List[Command] = commands
        self.dump: bool = dump


class Interrupted(Exception):
    def __init__(self: Self, dump: bool) -> None:
        super().__init__(f"Interrupted(dump={dump})")
        self.dump = dump


class Connection:
    def __init__(self: Self, serial: Serial, executor: Executor) -> None:
        self.serial: Serial = serial
        self._executor: Executor = executor
        self._command_queue: queue.Queue[Command] = queue.Queue(maxsize=0)
        self._interrupt_queue: queue.Queue[Interrupt] = queue.Queue(maxsize=1)
        self._error_queue: queue.Queue[Exception] = queue.Queue(maxsize=0)

        self._running: bool = True
        self._executor.submit(self._worker)
        logger.debug("Connection established")

    def shutdown(self: Self) -> None:
        """
        Shut down the connection.
        """

        self._running = False

    def write(self: Self, commands: Sequence[Command]) -> None:
        """
        Write to the serial port.

        Commands are buffered, respecting the ImageWriter II's CTS signal.
        """

        for command in commands:
            self._command_queue.put(command)

    def flush(self: Self) -> None:
        """
        Flush the underlying serial connection.
        """

        self.serial.flush()
        try:
            exc = self._error_queue.get_nowait()
            raise exc
        except queue.Empty:
            pass

    def interrupt(self: Self, commands: Sequence[Command], dump: bool = True) -> None:
        """
        Interrupt with a sequence of commands.

        Interrupts are run before any in-flight commands, and ignore the
        ImageWriter II's CTS line.
        """

        self._interrupt_queue.put_nowait(Interrupt(commands=list(commands), dump=dump))

    @property
    def _timeout(self: Self) -> float:
        return 1 / self.serial.baudrate

    def _worker(self: Self) -> None:
        try:
            while self._running:
                try:
                    # Check for interrupts
                    self._run_interrupts()
                    try:
                        # Fetch the command
                        command = self._command_queue.get(timeout=self._timeout)
                        # Check for interrupts again
                        self._run_interrupts()
                        # Wait for CTS to go high
                        self._wait_for_cts()
                        # Now we can write the command
                        self.serial.write(bytes(command))
                    except queue.Empty:
                        # No ready command - that's OK
                        continue
                except Interrupted as exc:
                    # Dump the command queue if need be
                    if exc.dump:
                        self._dump()
                    pass
        except Exception as exc:
            logger.error(exc)
            self._error_queue.put(exc)

    def _wait_for_cts(self: Self) -> None:
        # Check for interrupts until CTS is high
        while not self.serial.cts:
            time.sleep(self._timeout)
            self._run_interrupts()
        # Check for interrupts one last time
        self._run_interrupts()

    def _set_flow_control(self: Self, enabled: bool) -> None:
        if self.serial.protocol == SerialProtocol.XONXOFF:
            self.serial.xonxoff = enabled
        else:
            self.serial.rtscts = enabled

    def _run_interrupts(self: Self) -> None:
        try:
            # Is there an interrupt?
            interrupt = self._interrupt_queue.get_nowait()

            # Disable flow control
            self._set_flow_control(False)

            # Write our interrupt to the serial
            for command in interrupt.commands:
                self.serial.write(bytes(command))

            # Flush the serial
            self.flush()

            # Enable flow_control again
            self._set_flow_control(True)

            # Let the worker handle the cleanup
            raise Interrupted(interrupt.dump)
        except queue.Empty:
            # No interrupt, keep on truckin'
            pass

    def _dump(self: Self) -> None:
        # Pull from the command queue until exhausted
        try:
            while True:
                self._command_queue.get_nowait()
        except queue.Empty:
            pass
