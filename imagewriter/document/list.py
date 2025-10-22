from dataclasses import dataclass
from enum import Enum
from typing import List

from imagewriter.document.base import Block, Inline


class ListNumberStyle(Enum):
    """
    Style of list numbers.
    """

    DEFAULT = 0
    EXAMPLE = 1
    DECIMAL = 2
    LOWER_ROMAN = 3
    UPPER_ROMAN = 4
    LOWER_ALPHA = 5
    UPPER_ALPHA = 6


class ListNumberDelim(Enum):
    """
    Delimiter of list numbers.
    """

    DEFAULT = 0
    PERIOD = 1
    ONE_PAREN = 2
    TWO_PARENS = 3


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
