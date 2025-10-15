"""
Select and deselect commands are equivalent to toggling the SELECT button on
the front panel of the ImageWriter II. As per page 42 of the ImageWriter II
Owner's Manual, the printer will stop responding to commands other than
deselect.

Note that, when selected, the ImageWriter II will set its DTR signal to false,
meaning any device using software select will need to ignore its DTR signal
(typically wired to the CTS line under rs-232) in order to deselect the
printer.

By default, the ImageWriter II will not respond to these commands. To enable
them, open the "software select response" software switch.

See page 87 of the ImageWriter II Technical Reference Manual for more details.
"""

from imagewriter.encoding.base import Ctrl

SELECT = Ctrl("Q")
DESELECT = Ctrl("S")
