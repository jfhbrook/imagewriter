from dataclasses import dataclass
from typing import List, Tuple

from imagewriter.document.base import (
    Attr,
    Block,
    Caption,
    Format,
    Inline,
)
from imagewriter.document.list import ListAttributes
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


class CodeBlock(Block):
    """
    Code block (literal) with attributes.
    """

    attr: Attr
    contents: str


class RawBlock(Block):
    """
    Raw block.
    """

    format: Format
    contents: str


class BlockQuote(Block):
    """
    Block quote.
    """

    contents: List[Block]


class OrderedList(Block):
    """
    Ordered list.
    """

    attrs: ListAttributes
    items: List[List[Block]]


class BulletList(Block):
    """
    Bullet list.
    """

    items: List[List[Block]]


class DefinitionList(Block):
    """
    Definition list.
    """

    items: List[Tuple[List[Inline], List[List[Block]]]]


class Header(Block):
    """
    Header.
    """

    level: int
    attr: Attr
    contents: List[Inline]


class HorizontalRule(Block):
    """
    Horizontal rule.
    """

    pass


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


class Figure(Block):
    """
    Figure.
    """

    attr: Attr
    caption: Caption
    contents: List[Block]


class Div(Block):
    """
    Generic block container.
    """

    attr: Attr
    contents: List[Block]
