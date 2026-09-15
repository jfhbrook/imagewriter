"""
IPyWidgets for use with the ImageWriter II. These allow for hybrid coding/UI
interaction with the ImageWriter II in Jupyter.

The most useful widget for everyday use is `ControlPanel` as exported by this module.
This widget is built from the other widgets contained in submodules.
"""

from typing import List

from imagewriter.widgets.control import ControlPanel

# from imagewriter.widgets.connection import ActivityWidget, ConnectionWidget

__all__: List[str] = [
    "ControlPanel",
]
