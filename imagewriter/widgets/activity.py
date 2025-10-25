from typing import Optional, Self

import ipywidgets as widgets

import imagewriter.debug as debug
from imagewriter.serial import Serial
from imagewriter.widgets.base import Label


class SerialStateObserver(debug.SerialStateObserver):
    def __init__(self: Self, serial: Serial, widget: "ActivityWidget") -> None:
        self._widget = widget
        super().__init__(serial)

    def on_change(self: Self) -> None:
        self._widget.dtr.value = self._fmt_signal(self.serial.dtr)
        self._widget.dsr.value = self._fmt_signal(self.serial.dsr)
        self._widget.rts.value = self._fmt_signal(self.serial.rts)
        self._widget.cts.value = self._fmt_signal(self.serial.cts)


class ActivityWidget(widgets.VBox):
    def __init__(self: Self) -> None:
        self.dtr = widgets.Text(value="", disabled=True)
        self.dsr = widgets.Text(value="", disabled=True)
        self.rts = widgets.Text(value="", disabled=True)
        self.cts = widgets.Text(value="", disabled=True)

        super().__init__(
            [
                widgets.HBox(
                    [
                        Label(value="DTR:"),
                        self.dtr,
                    ]
                ),
                widgets.HBox(
                    [
                        Label(value="DSR:"),
                        self.dsr,
                    ]
                ),
                widgets.HBox(
                    [
                        Label(value="RTS:"),
                        self.rts,
                    ]
                ),
                widgets.HBox(
                    [
                        Label(value="CTS:"),
                        self.cts,
                    ]
                ),
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
        self.dtr = widgets.Text(value="")
        self.dsr = widgets.Text(value="")
        self.rts = widgets.Text(value="")
        self.cts = widgets.Text(value="")

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
