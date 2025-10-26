from typing import Protocol, Self

import ipywidgets as widgets


class TestPageCallback(Protocol):
    def __call__(self: Self, widget: "TestPageWidget") -> None: ...


class TestPageWidget(widgets.Button):
    def __init__(self: Self) -> None:
        super().__init__(
            description="Print Test Page",
            disabled=False,
            button_style="",
            tooltip="Print a test page.",
        )

    def on_print(self: Self, callback: TestPageCallback) -> None:
        def cb(button: widgets.Button) -> None:
            callback(self)

        self.on_click(cb)
