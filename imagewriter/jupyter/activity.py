from typing import Self

import ipywidgets as widgets

import imagewriter.debug as debug
from imagewriter.jupyter.connection import Connection


class SerialStateObserver(debug.SerialStateObserver):
    def __init__(self: Self, widget: "Activity") -> None:
        self._widget = widget
        self._port = widget._connection.port
        super().__init__(self._port)

    def on_change(self: Self) -> None:
        self._widget.dtr.value = self._fmt_signal(self.serial.dtr)
        self._widget.dsr.value = self._fmt_signal(self.serial.dsr)
        self._widget.rts.value = self._fmt_signal(self.serial.rts)
        self._widget.cts.value = self._fmt_signal(self.serial.cts)


class Activity(widgets.VBox):
    def __init__(self: Self, connection: Connection) -> None:
        self._connection: Connection = connection
        self.dtr: widgets.Text = widgets.Text(value="")
        self.dsr: widgets.Text = widgets.Text(value="")
        self.rts: widgets.Text = widgets.Text(value="")
        self.cts: widgets.Text = widgets.Text(value="")

        super().__init__(
            [
                widgets.HBox(
                    [
                        widgets.Label("DTR:"),
                        self.dtr,
                    ]
                ),
                widgets.HBox(
                    [
                        widgets.Label("DSR:"),
                        self.dsr,
                    ]
                ),
                widgets.HBox(
                    [
                        widgets.Label("RTS:"),
                        self.rts,
                    ]
                ),
                widgets.HBox(
                    [
                        widgets.Label("CTS:"),
                        self.cts,
                    ]
                ),
            ]
        )

        self._observer: SerialStateObserver = SerialStateObserver(self)
        self.start()

    def start(self: Self) -> None:
        self._observer.start()

    def stop(self: Self) -> None:
        self._observer.stop()
