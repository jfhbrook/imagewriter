from imagewriter.encoding.switch import CloseSoftwareSwitches, OpenSoftwareSwitches
from imagewriter.switch import SoftwareSwitch

"""
Ignore or respect the eighth data bit of each byte sent, as per page 34 of the
ImageWriter II Technical Reference Manual.

This setting is for the benefit of Applesoft Basic, which does not
support an eighth bit. Pure ASCII does not use the eighth bit, and the
ImageWriter II supports escape sequences for "high-ASCII", as per
Chapter 4 and Chapter 7 of the manual.

Note that the ImageWriter II will automatically switch to 8-bit mode
when an escape sequence sent to it uses 8-bit data - examples include
custom characters and graphics.
"""

IGNORE_EIGHTH_DATA_BIT = CloseSoftwareSwitches({SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT})
INCLUDE_EIGHTH_DATA_BIT = OpenSoftwareSwitches({SoftwareSwitch.IGNORE_EIGHTH_DATA_BIT})
