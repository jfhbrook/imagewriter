from dataclasses import dataclass
from enum import Enum
from typing import List

from imagewriter.document.base import Block, Inline


class ListNumberStyle(Enum):
    """
    Style of list numbers.
    """

    DEFAULT = "DefaultStyle"
    EXAMPLE = "Example"
    DECIMAL = "Decimal"
    LOWER_ROMAN = "LowerRoman"
    UPPER_ROMAN = "UpperRoman"
    LOWER_ALPHA = "LowerAlpha"
    UPPER_ALPHA = "UpperAlpha"


class ListNumberDelim(Enum):
    """
    Delimiter of list numbers.
    """

    DEFAULT = "DefaultDelim"
    PERIOD = "Period"
    ONE_PAREN = "OneParen"
    TWO_PARENS = "TwoParens"


@dataclass
class ListAttributes:
    """
    List attributes.
    """

    start: int
    style: ListNumberStyle
    delimiter: ListNumberDelim


@dataclass
class DefinitionListItem:
    term: List[Inline]
    definitions: List[List[Block]]
