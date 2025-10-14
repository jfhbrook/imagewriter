"""
Request that the ImageWriter II send an ID string, as per page 88 of the
ImageWriter II Technical Reference Manual.

Note that the request will not be handled until the printer receives a print
command.

Receiving the response has a number of additional caveats. See the
`imagewriter.identification` module for more details.
"""

from imagewriter.encoding.base import esc

REQUEST_SELF_IDENTIFY = esc("?")
