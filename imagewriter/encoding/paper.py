from imagewriter.encoding.base import esc

"""
Control of the paper-out sensor, as per page 74 of the ImageWriter II
Technical Reference Manual.

When enabled (the default), if the printer runs out of paper, the error light
will come on and the printer will become "deselected". This is presumably a
change in the serial status.

Note that installing a SheetFeeder will change the behavior to trigger sheet
feeds.
"""

ENABLE_PAPER_OUT_SENSOR = esc("O")
DISABLE_PAPER_OUT_SENSOR = esc("o")
