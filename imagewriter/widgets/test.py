from typing import List, Protocol, Self

import ipywidgets as widgets

from imagewriter.connection import Connection
from imagewriter.encoding import Command
from imagewriter.memory import print_buffer_size
from imagewriter.serial import Serial
from imagewriter.test import test_memory


class TestPageStatusWidget(widgets.Label):
    RUNNING = "⏳"
    ERROR = "❌ Error: {err}"

    def __init__(self: Self) -> None:
        super().__init__(value="")

    def running(self: Self) -> None:
        print("set to running")
        self.value = self.RUNNING

    def clear(self: Self) -> None:
        print("cleared")
        self.value = ""

    def error(self: Self, err: Exception) -> None:
        print(err)
        self.value = self.ERROR.format(err=err)


class MemoryTestStatusWidget(widgets.Label):
    RUNNING = "⏳"
    RESULT = "✅ Printer accepted {memory} bytes"
    ERROR = "❌ Error: {err}"

    def __init__(self: Self) -> None:
        super().__init__(value="")

    def running(self: Self) -> None:
        self.value = self.RUNNING

    def result(self: Self, memory: int) -> None:
        self.value = self.RESULT.format(memory=memory)

    def error(self: Self, err: Exception) -> None:
        self.value = self.ERROR.format(err=err)


class TestPageButtonWidget(widgets.Button):
    def __init__(self: Self) -> None:
        super().__init__(
            description="Print Test Page",
            disabled=False,
            button_style="",
            tooltip="Print a test page.",
        )


class MemoryTestButtonWidget(widgets.Button):
    def __init__(self: Self) -> None:
        super().__init__(
            description="Run Memory Test",
            disabled=False,
            button_style="",
            tooltip="Run a test to measure the size of the memory buffer",
        )


class TestCallback(Protocol):
    def __call__(self: Self, widget: "TestWidget") -> None: ...


class TestWidget(widgets.VBox):
    def __init__(self: Self) -> None:
        self._test_page_button_widget = TestPageButtonWidget()
        self._test_page_status_widget = TestPageStatusWidget()
        self._memory_test_button_widget = MemoryTestButtonWidget()
        self._memory_test_status_widget = MemoryTestStatusWidget()

        super().__init__(
            [
                widgets.HBox(
                    [
                        self._test_page_button_widget,
                        self._test_page_status_widget,
                    ]
                ),
                widgets.HBox(
                    [
                        self._memory_test_button_widget,
                        self._memory_test_status_widget,
                    ]
                ),
            ]
        )

    def print_test_page(
        self: Self, connection: Connection, test_page: List[Command]
    ) -> None:
        self._test_page_status_widget.running()
        try:
            connection.write(test_page).result()
        except Exception as exc:
            self._test_page_status_widget.error(exc)
            raise exc
        self._test_page_status_widget.clear()

    def run_memory_test(self: Self, serial: Serial, connection: Connection) -> None:
        self._memory_test_status_widget.running()
        try:
            memory = test_memory(serial, connection, print_buffer_size(True))
        except Exception as exc:
            self._memory_test_status_widget.error(exc)
            raise exc
        self._memory_test_status_widget.result(memory)

    def on_print(self: Self, callback: TestCallback) -> None:
        print("on_print method called")

        def cb(button: widgets.Button) -> None:
            callback(self)

        self._test_page_button_widget.on_click(cb)

    def on_memory_test(self: Self, callback: TestCallback) -> None:
        def cb(button: widgets.Button) -> None:
            callback(self)

        self._memory_test_button_widget.on_click(cb)
