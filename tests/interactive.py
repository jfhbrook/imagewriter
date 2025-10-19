from documents.attributes import ATTRIBUTES_TEST
from documents.hello import HELLO_WORLD
from IPython.display import Markdown

from imagewriter.encoding import CANCEL_CURRENT_LINE, CR, SetLFWhenLineFull
from imagewriter.serial import SerialError
from imagewriter.widgets import ControlPanel


def ensure_open(control: ControlPanel) -> None:
    try:
        control.open_port()
    except SerialError:
        pass


def test_hello_world(control: ControlPanel) -> Markdown:
    for command in HELLO_WORLD:
        control.port.write(bytes(command))

    control.port.flush()

    return Markdown('✅ "Hello World!"')


def test_attributes(control: ControlPanel) -> Markdown:
    for command in ATTRIBUTES_TEST:
        control.port.write(bytes(command))

    control.port.flush()

    return Markdown("✅ Attributes demo")


def test_memory(control: ControlPanel, print_buffer_size: int) -> Markdown:
    control.port.write(bytes(SetLFWhenLineFull(False)))
    control.port.write(bytes(CR))
    control.port.flush()

    i = 0

    while control.port.cts and i <= 2 * print_buffer_size:
        control.port.write(b"x")
        i += 1

    control.port.rtscts = False
    control.port.write(bytes(CANCEL_CURRENT_LINE))
    control.port.write(bytes(CR))
    control.port.flush()
    control.port.rtscts = True

    return Markdown(f"✅ Printer accepted **{i}** bytes")
