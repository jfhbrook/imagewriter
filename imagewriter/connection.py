from concurrent.futures import Executor, ThreadPoolExecutor
import queue
import time
from typing import List, Self, Sequence

from imagewriter.encoding import Command
from imagewriter.serial import Serial, SerialProtocol


class Interrupt:
    def __init__(self: Self, commands: List[Command], dump: bool) -> None:
        self.commands: List[Command] = commands
        self.dump: bool = dump


class Interrupted(Exception):
    def __init__(self: Self, dump: bool) -> None:
        super().__init__(f"Interrupted(dump={dump})")
        self.dump = dump


class Connection:
    def __init__(self: Self, port: Serial) -> None:
        self.port: Serial = port
        self._executor: Executor = ThreadPoolExecutor()
        self._command_queue: queue.Queue[Command] = queue.Queue(maxsize=0)
        self._interrupt_queue: queue.Queue[Interrupt] = queue.Queue(maxsize=1)

        self._running: bool = True
        self._executor.submit(self._worker)

    def shutdown(self: Self) -> None:
        """
        Shut down the background worker.
        """

        self._running = False
        self._executor.shutdown()

    def write(self: Self, commands: Sequence[Command]) -> None:
        """
        Write to the serial port.

        Commands are buffered, respecting the ImageWriter II's CTS signal.
        """

        for command in commands:
            self._command_queue.put(command)

    def interrupt(self: Self, commands: Sequence[Command], dump: bool = True) -> None:
        """
        Interrupt with a sequence of commands.

        Interrupts are run before any in-flight commands, and ignore the
        ImageWriter II's CTS line.
        """

        self._interrupt_queue.put_nowait(Interrupt(commands=list(commands), dump=dump))

    @property
    def _timeout(self: Self) -> float:
        return 1 / self.port.baudrate

    def _worker(self: Self) -> None:
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
                    self.port.write(bytes(command))
                except queue.Empty:
                    # No ready command - that's OK
                    continue
            except Interrupted as exc:
                # Dump the command queue if need be
                if exc.dump:
                    self._dump()
                pass

    def _wait_for_cts(self: Self) -> None:
        # Check for interrupts until CTS is high
        while not self.port.cts:
            time.sleep(self._timeout)
            self._run_interrupts()
        # Check for interrupts one last time
        self._run_interrupts()

    def _set_flow_control(self: Self, enabled: bool) -> None:
        if self.port.protocol == SerialProtocol.XONXOFF:
            self.port.xonxoff = enabled
        else:
            self.port.rtscts = enabled

    def _run_interrupts(self: Self) -> None:
        try:
            # Is there an interrupt?
            interrupt = self._interrupt_queue.get_nowait()

            # Disable flow control
            self._set_flow_control(False)

            # Write our interrupt to the port
            for command in interrupt.commands:
                self.port.write(bytes(command))

            # Flush the port
            self.port.flush()

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
