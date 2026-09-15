"""
Data modeling for print head motion.
"""

from enum import Enum
from typing import Literal

FormLength = Literal[11] | Literal[12]
LinesPerInch = Literal[6] | Literal[8]


class LineFeedDirection(Enum):
    """
    The line feed direction.
    """

    FORWARD = "Forward"
    REVERSE = "Reverse"
