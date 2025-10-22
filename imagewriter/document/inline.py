from dataclasses import dataclass
from typing import Any, List, Protocol, Self

from imagewriter.document.base import (
    Attr,
    Block,
    Format,
    Inline,
)
from imagewriter.document.citation import Citation
from imagewriter.document.link import Target
from imagewriter.document.math import MathType
from imagewriter.document.quote import QuoteType


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
