from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple

Format = str


class Inline:
    """
    Inline element.
    """

    pass


class Block:
    """
    Block element.
    """

    pass


@dataclass
class Attr:
    """
    Attributes.
    """

    identifier: str
    classes: List[str]
    pairs: List[Tuple[str, str]]


@dataclass
class Caption:
    """
    The caption of a table or figure.
    """

    short: "Optional[List[Inline]]"
    contents: "List[Block]"


class QuoteType(Enum):
    """
    Type of quotation marks to use in a quoted inline.
    """

    SINGLE_QUOTE = 0
    DOUBLE_QUOTE = 1


class MathType(Enum):
    """
    Type of math element.
    """

    DISPLAY = 0
    INLINE = 1
