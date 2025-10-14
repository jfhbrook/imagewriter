from concurrent.futures import ThreadPoolExecutor
import logging
import time
from typing import Optional, Self

from imagewriter.serial import Serial

logger: logging.Logger = logging.getLogger(__name__)


class FlowControlLogger:
    def __init__(self: Self, serial: Serial, executor: ThreadPoolExecutor) -> None:
        self._serial: Serial = serial
        self._executor: ThreadPoolExecutor = executor
        self._running: bool = False

    def _fmt_signal(self: Self, signal: bool) -> str:
        return "1" if signal else "0"

    def _fmt_change(self: Self, name: str, from_: Optional[bool], to: bool) -> str:
        formatted = f"{name}: "

        if from_ is None:
            formatted += self._fmt_signal(to)
        else:
            formatted += f"{self._fmt_signal(from_)} -> {self._fmt_signal(to)}"

        return formatted

    def _loop(self: Self) -> None:
        rts: Optional[bool] = None
        cts: Optional[bool] = None

        while self._running:
            if rts != self._serial.rts:
                print(self._fmt_change("RTS", rts, self._serial.rts))
            if cts != self._serial.cts:
                print(self._fmt_change("CTS", rts, self._serial.rts))
            time.sleep(1 / self._serial.baudrate)

    def start(self: Self) -> None:
        self._running = True
        self._executor.submit(self._loop)

    def stop(self: Self) -> None:
        self._running = False
