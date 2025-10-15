"""
When ^X is encountered anywhere in the currently buffered line, that line will
not be printed on the next Print Command.

See page 85 of the ImageWriter II Technical Reference Manual for more details.
"""

from imagewriter.encoding.base import Ctrl

CANCEL_CURRENT_LINE = Ctrl("X")
