from concurrent.futures import ThreadPoolExecutor
import datetime
import time
from typing import Optional, Self

from imagewriter.serial import Serial


class FlowControlLogger:
    def __init__(self: Self, serial: Serial) -> None:
        self.serial: Serial = serial
        self._executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)
        self._tick: float = 0.25 / serial.baudrate
        self.running: bool = False

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
        print(self._fmt_signal("dtr", self.serial.dtr))
        print(self._fmt_signal("dsr", self.serial.dsr))
        print(self._fmt_signal("rts", self.serial.rts))
        print(self._fmt_signal("cts", self.serial.cts))
        print("|-----------------|")
        print()

    def _loop(self: Self) -> None:
        dtr: Optional[bool] = None
        dsr: Optional[bool] = None
        rts: Optional[bool] = None
        cts: Optional[bool] = None

        while self.running:
            if any(
                [
                    dtr != self.serial.dtr,
                    dsr != self.serial.dsr,
                    rts != self.serial.rts,
                    cts != self.serial.cts,
                ]
            ):
                self._print_signals()

                dtr = self.serial.dtr
                dsr = self.serial.dsr
                rts = self.serial.rts
                cts = self.serial.cts

            time.sleep(self._tick)

    def start(self: Self) -> None:
        if self.running:
            return

        self.running = True
        self._executor.submit(self._loop)

    def stop(self: Self) -> None:
        self.running = False

    def shutdown(self: Self) -> None:
        self.stop()
        self._executor.shutdown()
