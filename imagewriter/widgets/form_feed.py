from typing import Protocol, Self

import ipywidgets as widgets

from imagewriter.connection import Connection
from imagewriter.encoding import SET_TOP_OF_FORM


class TopOfFormStatusWidget(widgets.Label):
    RUNNING = "⏳"
    ERROR = "❌ Error: {err}"

    def __init__(self: Self) -> None:
        super().__init__(value="")

    def running(self: Self) -> None:
        self.value = self.RUNNING

    def clear(self: Self) -> None:
        self.value = ""

    def error(self: Self, err: Exception) -> None:
        self.value = self.ERROR.format(err=err)


class TopOfFormButtonWidget(widgets.Button):
    def __init__(self: Self) -> None:
        super().__init__(
            description="Set Top Of Form",
            disabled=False,
            button_style="",
            tooltip="Set the current page position as the top of the form",
        )


class TopOfFormCallback(Protocol):
    def __call__(self: Self, widget: "TopOfFormWidget") -> None: ...


class TopOfFormWidget(widgets.HBox):
    def __init__(self: Self) -> None:
        self._button_widget = TopOfFormButtonWidget()
        self._status_widget = TopOfFormStatusWidget()

        super().__init__(
            [
                self._button_widget,
                self._status_widget,
            ]
        )

    def set_top_of_form(self: Self, connection: Connection) -> None:
        self._status_widget.running()
        try:
            connection.write([SET_TOP_OF_FORM])
        except Exception as exc:
            self._status_widget.error(exc)
            raise exc
        self._status_widget.clear()

    def on_set_top_of_form(self: Self, callback: TopOfFormCallback) -> None:
        def cb(button: widgets.Button) -> None:
            callback(self)

        self._button_widget.on_click(cb)
