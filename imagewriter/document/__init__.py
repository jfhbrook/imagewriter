from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Protocol, Self

from imagewriter.document.attr import Attr
from imagewriter.document.format import Format
from imagewriter.document.link import Target
from imagewriter.document.list import (
    ListAttributes,
    ListNumberDelim,
    ListNumberStyle,
)
from imagewriter.document.math import MathType
from imagewriter.document.quote import QuoteType
from imagewriter.document.table import Alignment, ColSpec

#
# Base types
#


class Inline(ABC):
    """
    Inline element.
    """

    @abstractmethod
    def accept[T](self: Self, visitor: "InlineVisitor[T]") -> T:
        pass


class InlineVisitor[T](Protocol):
    def visit_str(self: Self, element: "Str") -> T: ...
    def visit_emph(self: Self, element: "Emph") -> T: ...
    def visit_underline(self: Self, element: "Underline") -> T: ...
    def visit_strong(self: Self, element: "Strong") -> T: ...
    def visit_strikeout(self: Self, element: "Strikeout") -> T: ...
    def visit_subscript(self: Self, element: "Subscript") -> T: ...
    def visit_superscript(self: Self, element: "Superscript") -> T: ...
    def visit_small_caps(self: Self, element: "SmallCaps") -> T: ...
    def visit_quoted(self: Self, element: "Quoted") -> T: ...
    def visit_cite(self: Self, element: "Cite") -> T: ...
    def visit_code(self: Self, element: "Code") -> T: ...
    def visit_space(self: Self, element: "Space") -> T: ...
    def visit_soft_break(self: Self, element: "SoftBreak") -> T: ...
    def visit_line_break(self: Self, element: "LineBreak") -> T: ...
    def visit_math(self: Self, element: "Math") -> T: ...
    def visit_raw_inline(self: Self, element: "RawInline") -> T: ...
    def visit_link(self: Self, element: "Link") -> T: ...
    def visit_image(self: Self, element: "Image") -> T: ...
    def visit_note(self: Self, element: "Note") -> T: ...
    def visit_span(self: Self, element: "Span") -> T: ...


class Block(ABC):
    """
    Block element.
    """

    @abstractmethod
    def accept[T](self: Self, visitor: "BlockVisitor[T]") -> T:
        pass


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


#
# Captions
#


@dataclass
class Caption:
    """
    The caption of a table or figure.
    """

    short: Optional[List[Inline]]
    contents: List[Block]


#
# Citations
#


class Citation:
    pass


@dataclass
class CitationId(Citation):
    id: str


@dataclass
class CitationPrefix(Citation):
    prefix: List[Inline]


@dataclass
class CitationSuffix(Citation):
    suffix: List[Inline]


CitationModeType = (
    Literal["AuthorInText"] | Literal["SuppressAuthor"] | Literal["NormalCitation"]
)

AUTHOR_IN_TEXT: CitationModeType = "AuthorInText"
SUPPRESS_AUTHOR: CitationModeType = "SuppressAuthor"
NORMAL_CITATION: CitationModeType = "NormalCitation"


@dataclass
class CitationMode(Citation):
    mode: CitationModeType


@dataclass
class CitationNoteNum(Citation):
    number: int


@dataclass
class CitationHash(Citation):
    hash: int


#
# Table
#


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


@dataclass
class Str(Inline):
    """
    str.
    """

    contents: str

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_str(self)


@dataclass
class Emph(Inline):
    """
    Emphasized text.
    """

    contents: List[Inline]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_emph(self)


@dataclass
class Underline(Inline):
    """
    Underlined text.
    """

    contents: List[Inline]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_underline(self)


@dataclass
class Strong(Inline):
    """
    Strongly emphasized text.
    """

    contents: List[Inline]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_strong(self)


@dataclass
class Strikeout(Inline):
    """
    Strikeout text.
    """

    contents: List[Inline]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_strikeout(self)


@dataclass
class Subscript(Inline):
    """
    Subscripted text.
    """

    contents: List[Inline]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_subscript(self)


@dataclass
class Superscript(Inline):
    """
    Superscripted text.
    """

    contents: List[Inline]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_superscript(self)


@dataclass
class SmallCaps(Inline):
    """
    Small caps text.
    """

    contents: List[Inline]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_small_caps(self)


@dataclass
class Quoted(Inline):
    """
    Quoted text.
    """

    quote_type: QuoteType
    contents: List[Inline]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_quoted(self)


@dataclass
class Cite(Inline):
    """
    Citation.
    """

    citations: List[Citation]
    contents: List[Inline]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_cite(self)


@dataclass
class Code(Inline):
    """
    Inline code.
    """

    attr: Attr
    contents: str

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_code(self)


@dataclass
class Space(Inline):
    """
    Inter-word space.
    """

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_space(self)


@dataclass
class SoftBreak(Inline):
    """
    Soft line break.
    """

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_soft_break(self)


@dataclass
class LineBreak(Inline):
    """
    Hard line break.
    """

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_line_break(self)


@dataclass
class Math(Inline):
    """
    TeX math (literal).
    """

    math_type: MathType
    contents: str

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_math(self)


@dataclass
class RawInline(Inline):
    """
    Raw inline.
    """

    format: Format
    contents: str

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_raw_inline(self)


@dataclass
class Link(Inline):
    """
    Hyperlink.
    """

    attr: Attr
    alt_text: List[Inline]
    target: Target

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_link(self)


@dataclass
class Image(Inline):
    """
    Image.
    """

    attr: Attr
    alt_text: List[Inline]
    target: Target

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_image(self)


@dataclass
class Note(Inline):
    """
    Footnote or endnote.
    """

    contents: List[Block]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_note(self)


@dataclass
class Span(Inline):
    attr: Attr
    contents: List[Inline]

    def accept(self: Self, visitor: Any) -> Any:
        return visitor.visit_span(self)


#
# Blocks
#


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
class DefinitionListItem:
    term: List[Inline]
    definitions: List[List[Block]]


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


#
# Document
#


@dataclass
class Document:
    blocks: List[Block]
    pandoc_api_version: Optional[List[int]] = None
    meta: Optional[Dict[str, Any]] = None


#
# Exports
#

__all__: List[str] = [
    "Attr",
    "Block",
    "Document",
    "Format",
    "Inline",
    "BlockQuote",
    "BulletList",
    "CodeBlock",
    "DefinitionList",
    "Div",
    "Figure",
    "Header",
    "HorizontalRule",
    "LineBlock",
    "OrderedList",
    "Para",
    "Plain",
    "RawBlock",
    "Table",
    "Caption",
    "Citation",
    "CitationHash",
    "CitationId",
    "CitationMode",
    "CitationNoteNum",
    "CitationPrefix",
    "CitationSuffix",
    "Cite",
    "Code",
    "Emph",
    "Image",
    "LineBreak",
    "Link",
    "Math",
    "Note",
    "Quoted",
    "RawInline",
    "SmallCaps",
    "SoftBreak",
    "Space",
    "Str",
    "Strikeout",
    "Strong",
    "Subscript",
    "Superscript",
    "Underline",
    "Span",
    "Target",
    "DefinitionListItem",
    "ListAttributes",
    "ListNumberDelim",
    "ListNumberStyle",
    "MathType",
    "QuoteType",
    "Alignment",
    "Cell",
    "ColSpec",
    "Row",
    "TableBody",
    "TableFoot",
    "TableHead",
]
