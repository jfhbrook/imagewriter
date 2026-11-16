"""
Connection management for the ImageWriter II.
"""

import logging
import queue
from collections.abc import Generator, Sequence
from concurrent.futures import ALL_COMPLETED, Executor, Future, wait
from contextlib import contextmanager
from dataclasses import dataclass
from threading import Lock
from typing import Self

from imagewriter.encoding import Command
from imagewriter.serial import Serial

logger = logging.getLogger(__name__)


class ConnectionError(Exception):
    """
    A connection error.
    """


class ShutdownError(ConnectionError):
    pass


Count = int | None


class Counter:
    def __init__(self: Self) -> None:
        self.count: Count = None

    def add(self: Self, n: Count) -> None:
        if self.count is None:
            self.count = n
        elif n is not None:
            self.count += n


Result = Future[Count]


@dataclass
class Request:
    commands: list[Command]
    result: Result


class Connection:
    """
    A connection to an ImageWriter II printer.

    In the common case, we want to generally respect the flow control signal (via the
    CTS line in "hardware handshake" mode) while allowing to write past the buffer to
    write a complete command. This is handled by the `write` method.

    However, in certain situations, one may need to interrupt the stream of standard
    commands, even if the buffer is signaled to be full, with a command, typically to
    get the printer to clear the buffer. For example, sending a CR could trigger it to
    print out its current buffer, or a reset command could flush buffered commands and
    place the printer in a clean state. This is handled by the `interrupt` method.

    This class sends commands asynchronously, using a `concurrent.futures.Executor`.
    """

    def __init__(self: Self, serial: Serial, executor: Executor) -> None:
        self.serial: Serial = serial
        self._executor: Executor = executor

        self._lock = Lock()

        self._commands: queue.Queue[Request] = queue.Queue()
        self._interrupts: queue.Queue[Request] = queue.Queue()
        self._running = True

        self._workers = [
            self._executor.submit(self._command_worker),
            self._executor.submit(self._interrupt_worker),
        ]

        logger.debug("Connection established")

    def write(self: Self, commands: Sequence[Command]) -> Result:
        """
        Write to the serial port.

        Commands are buffered, generally respecting the ImageWriter II's CTS signal.
        """

        result: Result = Future()
        request = Request(list(commands), result)
        self._commands.put(request)

        logger.debug(f"Staged commands: {commands}")

        return result

    def interrupt(self: Self, commands: Sequence[Command]) -> Result:
        """
        Interrupt with a sequence of commands.

        Interrupts are run before any in-flight commands, and ignore the
        ImageWriter II's CTS line.
        """

        result: Result = Future()
        request = Request(list(commands), result)
        self._interrupts.put(request)

        logger.debug(f"Staged interrupts: {commands}")
        return result

    def shutdown(self: Self) -> None:
        self._running = False
        self._cancel_commands()
        self._cancel_interrupts()

        done, _ = wait(self._workers, return_when=ALL_COMPLETED)

        for fut in done:
            try:
                result = fut.result()
                assert result is None
            except ShutdownError:
                pass

    #
    # Commands
    #

    def _command_worker(self: Self) -> None:
        while self._running:
            try:
                request = self._commands.get_nowait()
                self._write_commands(request)
            except queue.Empty:
                logger.debug("Waiting for commands...")
                self.serial.tick()

    def _write_commands(self: Self, request: Request) -> None:
        commands = request.commands
        result = request.result

        counter = Counter()

        logger.debug(f"Received commands for write: {commands}")

        try:
            for command in commands:
                # Ensure CTS is asserted and the lock is acquired
                with self._command_session():
                    # Do the actual write
                    count = self.serial.write(bytes(command))
                counter.add(count)

            result.set_result(counter.count)
        except Exception as exc:  # noqa
            result.set_exception(exc)

    @contextmanager
    def _command_session(self: Self) -> Generator[None]:
        logger.debug("Waiting for CTS to be asserted...")

        while not self.serial.cts:
            if not self._running:
                raise ShutdownError("Shut down while waiting for asserted CTS")

            self.serial.tick()

        logger.debug("CTS is asserted. Acquiring lock to write command...")

        with self._lock:
            logger.debug("Lock acquired to write command")

            yield

        logger.debug("Lock released after writing command")

        self.serial.flush()

        logger.debug("Connection flushed after writing command")

    def _cancel_commands(self: Self) -> None:
        # Cancel all in-flight commands
        try:
            while True:
                request = self._commands.get_nowait()
                request.result.cancel()

                logger.debug(f"Commands canceled: {request.commands}")
        except queue.Empty:
            logger.debug("No commands canceled")

    #
    # Interrupts
    #

    def _interrupt_worker(self: Self) -> None:
        while self._running:
            logger.debug("Acquiring lock to run interrupts...")

            with self._lock:
                logger.debug("Lock to write interrupts acquired")

                self._run_interrupts()

            logger.debug("Lock released after writing interrupts")

            self.serial.tick()

    def _run_interrupts(self: Self) -> None:
        interrupted = False
        try:
            # Grab interrupts while they're there
            while True:
                request = self._interrupts.get_nowait()

                print("received interrupt")

                # An interrupt occurred
                interrupted = True

                # Run the interrupt
                self._write_interrupt(request)
        except queue.Empty:
            pass

        # Cancel in-flight commands if there were interrupts
        if interrupted:
            logger.debug("Interrupts executed - canceling remaining commands")

            self._cancel_commands()

    def _write_interrupt(self: Self, request: Request) -> None:
        counter = Counter()
        commands = request.commands
        result = request.result

        try:
            # Ignore RTS/CTS
            logger.debug("Entering interrupt mode...")

            with self.serial.interrupt_mode():
                # Write the commands
                for command in commands:
                    logger.debug(f"Writing interrupt: {command}")
                    count = self.serial.write(bytes(command))
                    counter.add(count)

            self.serial.flush()

            logger.debug("Connection flushed after writing interrupts")

            result.set_result(counter.count)
        except Exception as exc:  # noqa
            result.set_exception(exc)

    def _cancel_interrupts(self: Self) -> None:
        # Cancel all in-flight interrupts
        try:
            while True:
                request = self._interrupts.get_nowait()
                request.result.cancel()

                logger.debug(f"Interrupts canceled: {request.commands}")
        except queue.Empty:
            logger.debug("No interrupts canceled")
