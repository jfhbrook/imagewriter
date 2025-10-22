from dataclasses import dataclass
from typing import Any, List, Protocol, Self

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


class BlockVisitor[T](Protocol):
    def visit_plain(self: Self, element: "Plain") -> T: ...
    def visit_para(self: Self, element: "Para") -> T: ...
    def visit_line_block(self: Self, element: "LineBlock") -> T: ...
    def visit_code_block(self: Self, element: "CodeBlock") -> T: ...
    def visit_raw_block(self: Self, element: "RawBlock") -> T: ...
    def visit_block_quote(self: Self, element: "BlockQuote") -> T: ...
    def visit_ordered_list(self: Self, element: "OrderedList") -> T: ...
    def visit_bullet_list(self: Self, element: "BulletList") -> T: ...
    def visit_definition_list(self: Self, element: "DefinitionList") -> T: ...
    def visit_header(self: Self, element: "Header") -> T: ...
    def visit_horizontal_rule(self: Self, element: "HorizontalRule") -> T: ...
    def visit_table(self: Self, element: "Table") -> T: ...
    def visit_figure(self: Self, element: "Figure") -> T: ...
    def visit_div(self: Self, element: "Div") -> T: ...


@dataclass
class Plain(Block):
    """
    Plain text, not a paragraph.
    """

    contents: List[Inline]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_plain(self)


@dataclass
class Para(Block):
    """
    Paragraph.
    """

    contents: List[Inline]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_para(self)


@dataclass
class LineBlock(Block):
    """
    Multiple non-breaking lines.
    """

    contents: List[List[Inline]]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_line_block(self)


@dataclass
class CodeBlock(Block):
    """
    Code block (literal) with attributes.
    """

    attr: Attr
    contents: str

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_code_block(self)


@dataclass
class RawBlock(Block):
    """
    Raw block.
    """

    format: Format
    contents: str

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_raw_block(self)


@dataclass
class BlockQuote(Block):
    """
    Block quote.
    """

    contents: List[Block]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_block_quote(self)


@dataclass
class OrderedList(Block):
    """
    Ordered list.
    """

    attrs: ListAttributes
    items: List[List[Block]]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_ordered_list(self)


@dataclass
class BulletList(Block):
    """
    Bullet list.
    """

    items: List[List[Block]]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_bullet_list(self)


@dataclass
class DefinitionList(Block):
    """
    Definition list.
    """

    items: List[DefinitionListItem]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_definition_list(self)


@dataclass
class Header(Block):
    """
    Header.
    """

    level: int
    attr: Attr
    contents: List[Inline]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_header(self)


@dataclass
class HorizontalRule(Block):
    """
    Horizontal rule.
    """

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_horizontal_rule(self)


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

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_table(self)


@dataclass
class Figure(Block):
    """
    Figure.
    """

    attr: Attr
    caption: Caption
    contents: List[Block]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_figure(self)


@dataclass
class Div(Block):
    """
    Generic block container.
    """

    attr: Attr
    contents: List[Block]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_div(self)
