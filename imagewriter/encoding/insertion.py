from imagewriter.encoding.base import esc

"""
As per page 75 of the ImageWriter II Technical Reference Manual, when carriage
return insertion is enabled, an CR (\\r) will be inserted before every LF (\\n)
or FF (^L) character. This is enabled by default.

Note that this does not control whether or not LF or FF will trigger printing.
"""

ENABLE_CARRIAGE_RETURN_INSERTION = esc("l1")
DISABLE_CARRIAGE_RETURN_INSERTION = esc("l0")
