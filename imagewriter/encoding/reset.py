"""
Resetting the printer will do the following:

* Print all data currently in the print buffer
* Clear the print buffer
* Reset switches and other configuration to their defaults
* Clear custom characters

See page 87 of the ImageWriter II Technical Reference Manual for more details.
"""

from imagewriter.encoding.base import esc

RESET = esc("c")
