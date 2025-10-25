from documents.attributes import ATTRIBUTES_TEST
from documents.hello import HELLO_WORLD
from IPython.display import Markdown

from imagewriter.encoding import CANCEL_CURRENT_LINE, CR, Print, SetLFWhenLineFull
from imagewriter.widgets import ControlPanel


def test_hello_world(control: ControlPanel) -> Markdown:
    control.connection.write(HELLO_WORLD)
    control.connection.flush()

    return Markdown('✅ "Hello World!"')


def test_attributes(control: ControlPanel) -> Markdown:
    control.connection.write(ATTRIBUTES_TEST)
    control.connection.flush()

    return Markdown("✅ Attributes demo")


def test_memory(control: ControlPanel, print_buffer_size: int) -> Markdown:
    control.connection.write([SetLFWhenLineFull(False), CR])
    control.connection.flush()

    i = 0

    while control.serial.cts and i <= 2 * print_buffer_size:
        control.connection.write([Print(b"x")])
        i += 1

    control.serial.rtscts = False
    control.connection.write([CANCEL_CURRENT_LINE, CR])
    control.connection.flush()
    control.serial.rtscts = True

    return Markdown(f"✅ Printer accepted **{i}** bytes")
