from dataclasses import dataclass
from enum import Enum
from typing import List

from imagewriter.document.base import Attr, Block


class Alignment(Enum):
    """
    Alignment of a table column.
    """

    LEFT = 0
    RIGHT = 1
    CENTER = 2
    DEFAULT = 3


@dataclass
class ColSpec:
    """
    The specification for a single table column.
    """

    alignment: Alignment
    width: float = 1.0  # TODO: Is this a sensible default?


@dataclass
class Cell:
    """
    A table cell.
    """

    attr: Attr
    alignment: Alignment
    row_span: int
    column_span: int
    contents: List[Block]


@dataclass
class Row:
    """
    A table row.
    """

    attr: Attr
    contents: List[Cell]


@dataclass
class TableHead:
    """
    The head of a table.
    """

    attr: Attr
    rows: List[Row]


@dataclass
class TableBody:
    """
    A body of a table.
    """

    attr: Attr
    row_header_columns: int
    row_header: List[Row]
    body: List[Row]


@dataclass
class TableFoot:
    """
    The foot of a table.
    """

    attr: Attr
    rows: List[Row]
