from concurrent.futures import Executor, Future
import logging
import queue
from threading import Lock
import time
from typing import List, Optional, Self, Sequence, Tuple

from imagewriter.encoding import Command
from imagewriter.serial import Serial, SerialProtocol

logger = logging.getLogger(__name__)


class ConnectionError(Exception):
    pass


class InterruptError(ConnectionError):
    pass


InterruptRequest = Tuple[List[Command], Future[Optional[int]]]


def _add(a: Optional[int], b: Optional[int]) -> Optional[int]:
    if a is None:
        if b is None:
            return None
        return b
    elif b is None:
        return a
    else:
        return a + b


class Connection:
    def __init__(self: Self, serial: Serial, executor: Executor) -> None:
        self.serial: Serial = serial
        self._executor: Executor = executor
        self._command_lock = Lock()
        self._interrupts: queue.Queue[InterruptRequest] = queue.Queue()

    def write(self: Self, commands: Sequence[Command]) -> Future[Optional[int]]:
        return self._executor.submit(self._write, commands)

    def _write(self: Self, commands: Sequence[Command]) -> Optional[int]:
        count: Optional[int] = 0
        with self._command_lock:
            for command in commands:
                self._run_interrupts()

                while not self.serial.cts:
                    time.sleep(1 / self.serial.baudrate)
                    self._run_interrupts()

                res = self.serial.write(bytes(command))
                count = _add(count, res)

            self.serial.flush()
            return count

    def interrupt(self: Self, commands: Sequence[Command]) -> Future[Optional[int]]:
        fut: Future[Optional[int]] = Future()
        self._interrupts.put((list(commands), fut))
        return fut

    def _run_interrupts(self: Self) -> None:
        count: Optional[int] = None
        try:
            interrupts, fut = self._interrupts.get_nowait()
            try:
                self._set_flow_control(False)

                for command in interrupts:
                    res = self.serial.write(bytes(command))
                    count = _add(count, res)

                self._set_flow_control(True)

                self.serial.flush()

                fut.set_result(count)
            except Exception as exc:
                fut.set_exception(exc)

            raise InterruptError()
        except queue.Empty:
            pass

    def _set_flow_control(self: Self, enabled: bool) -> None:
        if self.serial.protocol == SerialProtocol.XONXOFF:
            self.serial.xonxoff = enabled
        else:
            self.serial.rtscts = enabled
