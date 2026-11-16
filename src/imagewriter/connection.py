"""
Connection management for the ImageWriter II.
"""

import logging
import queue
from collections.abc import Generator, Sequence
from concurrent.futures import ALL_COMPLETED, Executor, Future, wait
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Self

from imagewriter.encoding import Command
from imagewriter.serial import Serial

logger = logging.getLogger(__name__)


class Shutdown(Exception):
    pass


class Interrupted(Exception):
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
        self._commands: queue.Queue[Request] = queue.Queue()
        self._interrupts: queue.Queue[Request] = queue.Queue()

        self._running = True

        self._done = self._executor.submit(self._worker)

        logger.debug("Connection established")

    def shutdown(self: Self) -> None:
        """
        Shut down the connection.
        """

        self._running = False
        self._cancel(self._commands)
        self._cancel(self._interrupts)

        done, _ = wait([self._done], return_when=ALL_COMPLETED)

        for fut in done:
            try:
                fut.result()
            except Shutdown:
                pass

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

    def _worker(self: Self) -> None:
        #
        # The background worker. This pulls requests off the command and
        # interrupt queues.
        #

        while self._running:
            try:
                # Check for interrupts
                self._run_interrupts()
                try:
                    # Fetch the request
                    request = self._commands.get_nowait()

                    # Write the commands in the request
                    self._write_commands(request)
                except queue.Empty:
                    # No ready command - that's OK
                    logger.debug("Waiting for commands...")
                    self.serial.tick()
            except Interrupted:
                pass

        raise Shutdown()

    def _write_commands(self: Self, request: Request) -> None:
        #
        # Write commands.
        #

        commands = request.commands
        result = request.result

        counter = Counter()

        logger.debug(f"Received commands for write: {commands}")

        try:
            for command in commands:
                # CTS is asserted!
                with self._space():
                    # Do the actual write
                    count = self.serial.write(bytes(command))
                counter.add(count)

            result.set_result(counter.count)
        except Interrupted, Shutdown:
            result.set_result(counter.count)
            raise
        except Exception as exc:  # noqa
            result.set_exception(exc)

    def _run_interrupts(self: Self) -> None:
        #
        # Run any queued interrupt requests.
        #

        interrupted = False
        try:
            # Grab interrupts while they're there
            while True:
                request = self._interrupts.get_nowait()

                # An interrupt occurred
                interrupted = True

                # Run the interrupt
                self._write_interrupt(request)
        except queue.Empty:
            pass

        # Cancel in-flight commands if there were interrupts
        if interrupted:
            logger.debug("Interrupts executed - canceling remaining commands")

            self._cancel(self._commands)

            raise Interrupted()

    def _write_interrupt(self: Self, request: Request) -> None:
        #
        # Write an interrupt.
        #

        counter = Counter()
        commands = request.commands
        result = request.result

        logger.debug(f"Received commands for write: {commands}")

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
        except Interrupted, Shutdown:
            result.set_result(counter.count)
            raise
        except Exception as exc:  # noqa
            result.set_exception(exc)

    @contextmanager
    def _space(self: Self) -> Generator[None]:
        #
        # Create space for sending non-interrupt commands. This means waiting
        # for the CTS line to be asserted, and flushing the connection afterwards.
        #

        logger.debug("Waiting for CTS to be asserted...")

        self._breathe()

        while not self.serial.cts:
            self._breathe()
            self.serial.tick()

        logger.debug("CTS is asserted")

        self._breathe()

        yield

        self.serial.flush()

        self._breathe()

        logger.debug("Connection flushed after writing command")

    def _breathe(self: Self) -> None:
        #
        # Check that the worker isn't supposed to be running.
        #

        if not self._running:
            raise Shutdown()

    def _cancel(self: Self, requests: queue.Queue[Request]) -> None:
        #
        # Cancel all in-flight requests in a queue.
        #

        try:
            while True:
                request = requests.get_nowait()
                request.result.cancel()

                logger.debug(f"Request canceled: {request.commands}")
        except queue.Empty:
            logger.debug("No requests canceled")
