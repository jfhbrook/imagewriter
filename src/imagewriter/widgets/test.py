from typing import Protocol, Self

import ipywidgets as widgets  # type: ignore

from imagewriter.base.memory import print_buffer_size
from imagewriter.connection import Connection
from imagewriter.encoding import Command
from imagewriter.serial import Serial
from imagewriter.test import test_memory, TestPage

FULL_MONTY = "Full Monty!"

TEST_PAGES = {
    FULL_MONTY: "full_monty",
    "Languages": "languages",
    "Pitch": "pitch",
    "Quality": "quality",
    "Attributes": "attributes",
    "MouseText": "mousetext",
    "Markdown": "markdown",
}


class TestPageButtonWidget(widgets.Button):
    def __init__(self: Self) -> None:
        super().__init__(
            description="Print Test Page",
            disabled=False,
            button_style="",
            tooltip="Print the selected test page.",
        )


class TestPageSelectWidget(widgets.Dropdown):
    def __init__(self: Self) -> None:
        super().__init__(
            options=list(TEST_PAGES.keys()), value=FULL_MONTY, disabled=False
        )

    @property
    def page_name(self: Self) -> str:
        if not isinstance(self.value, str):
            return FULL_MONTY

        return TEST_PAGES[self.value]


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
        self._test_page_select_widget = TestPageSelectWidget()
        self._test_page_status_widget = TestPageStatusWidget()
        self._memory_test_button_widget = MemoryTestButtonWidget()
        self._memory_test_status_widget = MemoryTestStatusWidget()

        super().__init__(
            [
                widgets.HBox(
                    [
                        self._test_page_button_widget,
                        self._test_page_select_widget,
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
        self: Self, connection: Connection, test_page: TestPage
    ) -> None:
        commands: list[Command] = getattr(
            test_page, self._test_page_select_widget.page_name
        )()
        self._test_page_status_widget.running()
        try:
            for cmd in commands:
                connection.serial.write(bytes(cmd))

            # connection.write(test_page)
            connection.flush()
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
        def cb(button: widgets.Button) -> None:
            callback(self)

        self._test_page_button_widget.on_click(cb)

    def on_memory_test(self: Self, callback: TestCallback) -> None:
        def cb(button: widgets.Button) -> None:
            callback(self)

        self._memory_test_button_widget.on_click(cb)
