from typing import Any, Optional, Self

import ipywidgets as widgets

import imagewriter.debug as debug
from imagewriter.serial import Serial
from imagewriter.widgets.base import Label


class SignalWidget(widgets.HBox):
    def __init__(self: Self, name: str) -> None:
        self.signal = widgets.Text(value="🌑", disabled=True)

        super().__init__([Label(value=f"{name}:"), self.signal])

    @property
    def level(self: Self) -> bool:
        return self.signal.value == "🌕"

    @level.setter
    def level(self: Self, level: bool) -> None:
        self.signal.value = "🌕" if level else "🌑"

    def reset(self: Self) -> None:
        self.value = "🌑"


class WriteStatsWidget(widgets.HBox):
    def __init__(self: Self) -> None:
        self._written = 0
        self._written_widget = widgets.Label(value="0kb")

        super().__init__([Label("Written:"), self._written_widget])

    def on_write(self: Self, data: Any) -> None:
        self._written += len(data)
        self._written_widget.value = f"{self._written / 1024}kb"

    def reset(self: Self) -> None:
        self._written = 0
        self._written_widget.value = "0kb"


class SerialStateObserver(debug.SerialStateObserver):
    def __init__(self: Self, serial: Serial, widget: "ActivityWidget") -> None:
        self._widget = widget

        self._write_hook(serial)

        super().__init__(serial)

    def _on_write(self: Self, data: Any) -> None:
        self._widget.write_stats.on_write(data)

    def _write_hook(self: Self, serial: Serial) -> None:
        _write = serial.write

        def write(data: Any) -> Optional[int]:
            self._on_write(data)
            return _write(data)

        serial.write = write

    def on_change(self: Self) -> None:
        self._widget.dtr.level = self.serial.dtr
        self._widget.dsr.level = self.serial.dsr
        self._widget.rts.level = self.serial.rts
        self._widget.cts.level = self.serial.cts


class ActivityWidget(widgets.VBox):
    def __init__(self: Self) -> None:
        self.write_stats = WriteStatsWidget()

        self.dtr = SignalWidget("DTR")
        self.dsr = SignalWidget("DSR")
        self.rts = SignalWidget("RTS")
        self.cts = SignalWidget("CTS")

        super().__init__(
            [
                self.write_stats,
                self.dtr,
                self.dsr,
                self.rts,
                self.cts,
            ]
        )

        self._observer: Optional[SerialStateObserver] = None

    def instrument(self: Self, serial: Serial) -> None:
        self._reset()
        self._observer = SerialStateObserver(serial=serial, widget=self)
        self.start()

    def _reset(self: Self) -> None:
        if self._observer:
            self.shutdown()
        self.write_stats.reset()
        self.dtr.reset()
        self.dsr.reset()
        self.rts.reset()
        self.cts.reset()

    def start(self: Self) -> None:
        if self._observer:
            self._observer.start()

    def stop(self: Self) -> None:
        if self._observer:
            self._observer.stop()

    def shutdown(self: Self) -> None:
        if self._observer:
            self._observer.shutdown()
            self._observer = None
