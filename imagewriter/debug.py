from concurrent.futures import ThreadPoolExecutor
import datetime
import time
from typing import Optional, Self

from imagewriter.serial import Serial


class FlowControlLogger:
    def __init__(self: Self, serial: Serial, executor: ThreadPoolExecutor) -> None:
        self._serial: Serial = serial
        self._executor: ThreadPoolExecutor = executor
        self._tick: float = 0.25 / serial.baudrate
        self._running: bool = False

    def _timestamp(self: Self) -> str:
        return datetime.datetime.now().strftime("%H:%M:%S.%f")

    def _fmt_signal(self: Self, name: str, signal: bool) -> str:
        light = "🚨" if signal else "_"

        return f"| {name} | {light}         |"

    def _print_signals(self: Self) -> None:
        ts: str = self._timestamp()
        print()
        print("|-----------------|")
        print(f"| ${ts} |")
        print("|-----------------|")
        print(self._fmt_signal("dtr", self._serial.dtr))
        print(self._fmt_signal("dsr", self._serial.dsr))
        print(self._fmt_signal("rts", self._serial.rts))
        print(self._fmt_signal("cts", self._serial.cts))
        print("|-----------------|")
        print()

    def _loop(self: Self) -> None:
        dtr: Optional[bool] = None
        dsr: Optional[bool] = None
        rts: Optional[bool] = None
        cts: Optional[bool] = None

        while self._running:
            if any(
                [
                    dtr != self._serial.dtr,
                    dsr != self._serial.dsr,
                    rts != self._serial.rts,
                    cts != self._serial.cts,
                ]
            ):
                self._print_signals()

                dtr = self._serial.dtr
                dsr = self._serial.dsr
                rts = self._serial.rts
                cts = self._serial.cts

            time.sleep(self._tick)

    def start(self: Self) -> None:
        self._running = True
        self._executor.submit(self._loop)

    def stop(self: Self) -> None:
        self._running = False
