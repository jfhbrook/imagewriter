from conftest import HELLO_WORLD
from IPython.display import Markdown

import imagewriter.test as test
from imagewriter.widgets import ControlPanel


def test_hello_world(control: ControlPanel) -> Markdown:
    control.connection.write(HELLO_WORLD)
    control.connection.flush()

    return Markdown('✅ "Hello World!"')


def test_memory(control: ControlPanel, print_buffer_size: int) -> Markdown:
    memory = test.test_memory(control.serial, control.connection, print_buffer_size)

    return Markdown(f"✅ Printer accepted **{memory}** bytes")
