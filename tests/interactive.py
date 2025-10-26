from conftest import HELLO_WORLD
from IPython.display import Markdown

from imagewriter.widgets import ControlPanel


def test_hello_world(control: ControlPanel) -> Markdown:
    control.connection.write(HELLO_WORLD)
    control.connection.flush()

    return Markdown('✅ "Hello World!"')
