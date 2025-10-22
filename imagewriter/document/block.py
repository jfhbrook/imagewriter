from dataclasses import dataclass
from typing import List

from imagewriter.document.base import (
    Attr,
    Block,
    Format,
    Inline,
)
from imagewriter.document.caption import Caption
from imagewriter.document.list import DefinitionListItem, ListAttributes
from imagewriter.document.table import (
    ColSpec,
    TableBody,
    TableFoot,
    TableHead,
)


@dataclass
class Plain(Block):
    """
    Plain text, not a paragraph.
    """

    contents: List[Inline]


@dataclass
class Para(Block):
    """
    Paragraph.
    """

    contents: List[Inline]


@dataclass
class LineBlock(Block):
    """
    Multiple non-breaking lines.
    """

    contents: List[List[Inline]]


@dataclass
class CodeBlock(Block):
    """
    Code block (literal) with attributes.
    """

    attr: Attr
    contents: str


@dataclass
class RawBlock(Block):
    """
    Raw block.
    """

    format: Format
    contents: str


@dataclass
class BlockQuote(Block):
    """
    Block quote.
    """

    contents: List[Block]


@dataclass
class OrderedList(Block):
    """
    Ordered list.
    """

    attrs: ListAttributes
    items: List[List[Block]]


@dataclass
class BulletList(Block):
    """
    Bullet list.
    """

    items: List[List[Block]]


@dataclass
class DefinitionList(Block):
    """
    Definition list.
    """

    items: List[DefinitionListItem]


@dataclass
class Header(Block):
    """
    Header.
    """

    level: int
    attr: Attr
    contents: List[Inline]


@dataclass
class HorizontalRule(Block):
    """
    Horizontal rule.
    """

    pass


@dataclass
class Table(Block):
    """
    Table.
    """

    attr: Attr
    caption: Caption
    columns: List[ColSpec]
    header: TableHead
    body: List[TableBody]
    footer: TableFoot


@dataclass
class Figure(Block):
    """
    Figure.
    """

    attr: Attr
    caption: Caption
    contents: List[Block]


@dataclass
class Div(Block):
    """
    Generic block container.
    """

    attr: Attr
    contents: List[Block]
