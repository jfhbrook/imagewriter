from conftest import ATTRIBUTES, HELLO_WORLD, LANGUAGES, PITCHES, SIMPLE_MARKDOWN
from IPython.display import Markdown

from imagewriter.encoding import CANCEL_CURRENT_LINE, CR, Print, SetLFWhenLineFull
from imagewriter.pandoc import parse_document
from imagewriter.render import DocumentRenderer
from imagewriter.widgets import ControlPanel


def test_hello_world(control: ControlPanel) -> Markdown:
    control.connection.write(HELLO_WORLD)
    control.connection.flush()

    return Markdown('✅ "Hello World!"')


def test_attributes(control: ControlPanel) -> Markdown:
    control.connection.write(ATTRIBUTES)
    control.connection.flush()

    return Markdown("✅ Attributes")


def test_languages(control: ControlPanel) -> Markdown:
    control.connection.write(LANGUAGES)
    control.connection.flush()

    return Markdown("✅ Languages")


def test_pitches(control: ControlPanel) -> Markdown:
    control.connection.write(PITCHES)
    control.connection.flush()

    return Markdown("✅ Pitches")


def test_markdown(control: ControlPanel) -> Markdown:
    doc = parse_document(SIMPLE_MARKDOWN)
    renderer = DocumentRenderer(control.settings)
    commands = renderer.render(doc)

    control.connection.write(commands)
    control.connection.flush()

    return Markdown("✅ Markdown")


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
