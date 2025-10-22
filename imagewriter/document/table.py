from dataclasses import dataclass
from typing import List, Literal, Optional

from imagewriter.document.base import Attr, Block

Alignment = (
    Literal["AlignLeft"]
    | Literal["AlignRight"]
    | Literal["AlignCenter"]
    | Literal["AlignDefault"]
)


@dataclass
class ColSpec:
    """
    The specification for a single table column.
    """

    alignment: Alignment
    width: Optional[float]


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
